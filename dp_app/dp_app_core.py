from metadata import dataset as ds
from dp_app import settings as sc

import logging

from utils import file_io as uff
from utils import misc as ufm

import spacy

# from spacy import displacy
import spacy.cli

spacy.cli.download("en_core_web_sm")
# from spacy.tokenizer import Tokenizer
# from spacy.pipeline import EntityRuler
# from spacy.util import compile_infix_regex

import re
from functools import lru_cache

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
    logging.info("Loading the ML model")
    nlp = spacy.load("en_core_web_sm")
    # nlp.tokenizer = custom_tokenizer(nlp)
    # ruler = nlp.add_pipe("entity_ruler")
    # ruler.add_patterns([{"label": "SSN", "pattern": [{"TEXT": {"REGEX": r"^\d{3}\W\d{2}\W\d{4}$"}}]}])
    # Spacy splits the numbers at '-'. To avoid this, an existing rule is removed in custom_tokenizer(). This fixes the SSN but breaks the DATE recognition.
    # ruler.add_patterns([{"label": "DATE", "pattern": [{"TEXT": {"REGEX": r"^\d{4}\W\d{2}\W\d{2}$"}}]}])
    # ruler.add_patterns([{"label": "DATE", "pattern": [{"TEXT": {"REGEX": r"^\d{2}\W\d{2}\W\d{4}$"}}]}])

    return nlp


def apply_ner_model(dataset_id: str) -> list:

    # Simulate getting the dataset metadata from API
    dataset = ds.LocalDelimFileDataset.from_json(dataset_id)

    src_file_path = sc.resolve_app_path(dataset.file_path)
    src_file_records = uff.uf_read_delim_file_to_list_of_dict(file_path=src_file_path)

    # Load customized NLP NER model
    NER = load_customize_nlp_ner_model()

    # Profile the dataset
    dp_results = []
    for record in src_file_records:
        for k, v in record.items():
            mdl_out = NER(str(v))
            dp_result = fmt_dp_result(k, v, mdl_out)
            # print(dp_result)
            dp_results.append(dp_result)

    return ufm.dedupe_list_of_dict(dp_results)


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
