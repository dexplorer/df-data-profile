import logging
import os

import click
from dp_app import settings as sc
from dp_app import dp_app_core as dpc
from utils import logger as ufl


@click.command()
@click.option(
    "--dataset_id", type=str, default="dev", help="Source dataset id", required=True
)
@click.option("--env", type=str, default="dev", help="Environment")
def profile_dataset(dataset_id: str, env: str):
    """
    Profile the dataset.
    See ./log/dp_app_cli.log for logs.
    """

    cfg = sc.load_config(env)
    sc.set_config(cfg)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    logging.info("Start profiling the dataset %s", dataset_id)
    dp_results = dpc.apply_ner_model(dataset_id=dataset_id)

    logging.debug("Data profile results for dataset %s", dataset_id)
    logging.debug(dp_results)

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
