from metadata import dataset as ds
from app_calendar import eff_date as ed
from utils import spark_io as ufs

from config.settings import ConfigParms as sc

import logging

from utils import csv_io as ufc
from utils import misc as ufm

import spacy

# from spacy import displacy
import spacy.cli

# spacy.cli.download("en_core_web_sm")
# from spacy.tokenizer import Tokenizer
# from spacy.pipeline import EntityRuler
# from spacy.util import compile_infix_regex

import re
from functools import lru_cache


def apply_ner_model(dataset_id: str, cycle_date: str) -> list:
    # Simulate getting the cycle date from API
    # Run this from the parent app
    if not cycle_date:
        cycle_date = ed.get_cur_cycle_date()

    # Simulate getting the dataset metadata from API
    # dataset = ds.LocalDelimFileDataset.from_json(dataset_id)
    dataset = ds.get_dataset_from_json(dataset_id=dataset_id)

    # Get current effective date
    cur_eff_date = ed.get_cur_eff_date(
        schedule_id=dataset.schedule_id, cycle_date=cycle_date
    )
    cur_eff_date_yyyymmdd = ed.fmt_date_str_as_yyyymmdd(cur_eff_date)

    src_data_records = []
    if dataset.dataset_type == ds.DatasetType.LOCAL_DELIM_FILE:
        # Read the source data file
        src_file_path = sc.resolve_app_path(
            dataset.resolve_file_path(cur_eff_date_yyyymmdd)
        )
        logging.info("Reading the file %s", src_file_path)
        src_data_records = ufc.uf_read_delim_file_to_list_of_dict(
            file_path=src_file_path
        )

    elif dataset.dataset_type == ds.DatasetType.SPARK_TABLE:
        # Read the spark table
        qual_target_table_name = dataset.get_qualified_table_name()
        logging.info("Reading the spark table %s", qual_target_table_name)
        src_data_records = ufs.read_spark_table_into_list_of_dict(
            qual_target_table_name=qual_target_table_name,
            cur_eff_date=cur_eff_date,
            warehouse_path=sc.hive_warehouse_path,
        )

    # Load customized NLP NER model
    NER = load_customize_nlp_ner_model()

    # Profile the dataset
    dp_results = []
    for record in src_data_records:
        for k, v in record.items():
            mdl_out = NER(str(v))
            dp_result = fmt_dp_result(k, v, mdl_out)
            # print(dp_result)
            dp_results.append(dp_result)

    priority_list = ["PII", "NON PII"]
    dp_results_deduped = ufm.dedupe_list_of_dict_by_value_priority(
        records=dp_results,
        priority_list=priority_list,
        key_column="column_name",
        priority_column="data_class",
    )
    # dp_results_deduped = ufm.dedupe_list_of_dict(dp_results)

    return dp_results_deduped


# def custom_tokenizer(nlp):
#     # Take out the existing rule and replace it with a custom one:
#     inf = list(nlp.Defaults.infixes)
#     inf.remove(r"(?<=[0-9])[+\-\*^](?=[0-9-])")
#     inf = tuple(inf)
#     infixes = inf + tuple([r"(?<=[0-9])[+*^](?=[0-9-])", r"(?<=[0-9])-(?=-)"])
#     infix_re = compile_infix_regex(infixes)

#     return Tokenizer(
#         nlp.vocab,
#         prefix_search=nlp.tokenizer.prefix_search,
#         suffix_search=nlp.tokenizer.suffix_search,
#         infix_finditer=infix_re.finditer,
#         token_match=nlp.tokenizer.token_match,
#         rules=nlp.Defaults.tokenizer_exceptions,
#     )


@lru_cache(maxsize=1)
def load_customize_nlp_ner_model():
    logging.info("Downloading the ML model")
    spacy.cli.download("en_core_web_sm")

    logging.info("Loading the ML model")
    nlp = spacy.load("en_core_web_sm")
    # nlp.tokenizer = custom_tokenizer(nlp)
    # ruler = nlp.add_pipe("entity_ruler")
    # ruler.add_patterns([{"label": "SSN", "pattern": [{"TEXT": {"REGEX": r"^\d{3}\W\d{2}\W\d{4}$"}}]}])
    # Spacy splits the numbers at '-'. To avoid this, an existing rule is removed in custom_tokenizer(). This fixes the SSN but breaks the DATE recognition.
    # ruler.add_patterns([{"label": "DATE", "pattern": [{"TEXT": {"REGEX": r"^\d{4}\W\d{2}\W\d{2}$"}}]}])
    # ruler.add_patterns([{"label": "DATE", "pattern": [{"TEXT": {"REGEX": r"^\d{2}\W\d{2}\W\d{4}$"}}]}])

    return nlp


def get_data_class(col_name, col_val, mdl_labels):
    """
    Spacy NLP NER model output entity labels -
    PERSON:      People, including fictional.
    NORP:        Nationalities or religious or political groups.
    FAC:         Buildings, airports, highways, bridges, etc.
    ORG:         Companies, agencies, institutions, etc.
    GPE:         Countries, cities, states.
    LOC:         Non-GPE locations, mountain ranges, bodies of water.
    PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
    EVENT:       Named hurricanes, battles, wars, sports events, etc.
    WORK_OF_ART: Titles of books, songs, etc.
    LAW:         Named documents made into laws.
    LANGUAGE:    Any named language.
    DATE:        Absolute or relative dates or periods.
    TIME:        Times smaller than a day.
    PERCENT:     Percentage, including ”%“.
    MONEY:       Monetary values, including unit.
    QUANTITY:    Measurements, as of weight or distance.
    ORDINAL:     “first”, “second”, etc.
    CARDINAL:    Numerals that do not fall under another type.
    """

    data_class = "UNKNOWN"
    if "PERSON" in mdl_labels and "name" in col_name:
        info_type = "NAME"
        data_class = "PII"
    elif "LOC" in mdl_labels and ufm.check_if_any_list_item_in_str(
        ["address", "addr"], col_name
    ):
        info_type = "ADDRESS"
        data_class = "PII"
    elif "DATE" in mdl_labels and ufm.check_if_any_list_item_in_str(
        ["dob", "birth"], col_name
    ):
        info_type = "DATE OF BIRTH"
        data_class = "PII"
    elif "CARDINAL" in mdl_labels and re.match(r"^\d{3}\W\d{2}\W\d{4}$", col_val):
        info_type = "SSN"
        data_class = "PII"
    else:
        info_type = ", ".join(mdl_labels)
        data_class = "NON PII"

    return info_type, data_class


def fmt_dp_result(col_name, col_val, mdl_out) -> dict:
    mdl_labels = []
    for word in mdl_out.ents:
        # print(word.text,word.label_)
        mdl_labels.append(word.label_)

    info_type, data_class = get_data_class(col_name, col_val, mdl_labels)

    dp_result = {
        "column_name": col_name,
        "info_type": info_type,
        "data_class": data_class,
    }

    return dp_result
