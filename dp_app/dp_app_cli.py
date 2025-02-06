import logging
import os

import click
from dp_app.settings import ConfigParms as sc
from dp_app import dp_app_core as dpc
from utils import logger as ufl


@click.command()
@click.option(
    "--dataset_id", type=str, default="dev", help="Source dataset id", required=True
)
@click.option("--env", type=str, default="dev", help="Environment")
@click.option("--cycle_date", type=str, default="", help="Cycle date")
def profile_dataset(dataset_id: str, env: str, cycle_date: str):
    """
    Profile the dataset.
    """

    sc.load_config(env)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    logging.info("Start profiling the dataset %s", dataset_id)
    dp_results = dpc.apply_ner_model(dataset_id=dataset_id, cycle_date=cycle_date)

    logging.info("Data profile results for dataset %s", dataset_id)
    logging.info(dp_results)

    logging.info("Finished profiling the dataset %s", dataset_id)


# Create command group
@click.group()
def cli():
    pass


# Add sub command to group
cli.add_command(profile_dataset)


def main():
    cli()


if __name__ == "__main__":
    main()
