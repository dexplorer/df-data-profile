import logging
import os

import click
from dotenv import load_dotenv
from config.settings import ConfigParms as sc
from dp_app import dp_app_core as dpc
from utils import logger as ufl


# Create command group
@click.group()
def cli():
    pass


@cli.command()
@click.option("--dataset_id", type=str, help="Source dataset id", required=True)
@click.option("--cycle_date", type=str, default="", help="Cycle date")
def profile_dataset(dataset_id: str, cycle_date: str):
    """
    Profile the dataset.
    """

    logging.info("Start profiling the dataset %s", dataset_id)
    dp_results = dpc.apply_ner_model(dataset_id=dataset_id, cycle_date=cycle_date)

    logging.info("Data profile results for dataset %s", dataset_id)
    logging.info(dp_results)

    logging.info("Finished profiling the dataset %s", dataset_id)


def main():
    # Load the environment variables from .env file
    load_dotenv()

    # Fail if env variable is not set
    sc.load_config()

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.app_log_dir}/{script_name}.log")
    logging.info("Configs are set")
    logging.info(os.environ)
    logging.info(sc.config)
    logging.info(vars(sc))

    cli()


if __name__ == "__main__":
    main()
