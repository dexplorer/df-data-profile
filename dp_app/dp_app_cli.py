import logging
import os

import click
from dp_app import settings as sc
from dp_app import dp_app_core as dpc
from dp_app.utils import logger as ufl


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

    logging.info(f"Set configs")
    cfg = sc.load_config(env)
    sc.set_config(cfg)

    logging.info(f"Start profiling the dataset {dataset_id}")
    dp_results = dpc.apply_ner_model(dataset_id=dataset_id)

    click.echo(f"Data profile results for dataset {dataset_id}")
    click.echo(dp_results)

    logging.info(f"Finished profiling the dataset {dataset_id}")


# Create command group
@click.group()
def cli():
    pass


# Add sub command to group
cli.add_command(profile_dataset)


def main():
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_name=script_name)
    cli()


if __name__ == "__main__":
    main()
