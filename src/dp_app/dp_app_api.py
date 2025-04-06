import os
import logging

# from dotenv import load_dotenv, find_dotenv
from config.settings import ConfigParms as sc
from dp_app import dp_app_core as dpc
from utils import logger as ufl
import argparse
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    """
    Default route

    Args:
        none

    Returns:
        A default message.
    """

    return {"message": "Data Profiling App"}


@app.get("/profile-dataset/")
async def profile_dataset(dataset_id: str, cycle_date: str = ""):
    """
    Profile the dataset.

    Args:
        dataset_id: Id of the dataset.
        cycle_date: Cycle date

    Returns:
        Data classifications at column level.
    """

    logging.info("Start profiling the dataset %s", dataset_id)
    dp_results = dpc.apply_ner_model(dataset_id=dataset_id, cycle_date=cycle_date)
    logging.info("Finished profiling the dataset %s", dataset_id)

    return {"results": dp_results}


def main():
    parser = argparse.ArgumentParser(description="Data Profile Application")
    parser.add_argument(
        "--app_host_pattern",
        help="Environment where the application is hosted.",
        nargs=None,  # 1 argument values
        default="aws_ec2_native",  # default when the argument is not provided
        required=True,
    )
    parser.add_argument(
        "--debug",
        help="Set the logging level to DEBUG",
        nargs="?",  # 0-or-1 argument values
        const="y",  # default when the argument is provided with no value
        default="n",  # default when the argument is not provided
        required=False,
    )

    # Get the arguments
    args = vars(parser.parse_args())
    app_host_pattern = args["app_host_pattern"]
    debug = args["debug"]
    if debug == "y":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Set env anf cfg variables
    sc.load_config(app_host_pattern)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_multi_platform_logger(
        log_level=log_level,
        handlers=sc.log_handlers,
        log_file_path_name=f"{sc.app_log_dir}/{script_name}.log",
    )
    logging.info("Configs are set")
    logging.info(os.environ)
    logging.info(sc.config)
    logging.info(vars(sc))

    logging.info("Starting the API service")

    uvicorn.run(
        app,
        port=int(os.environ["API_PORT"]),
        host=os.environ["API_HOST"],
        log_config=None,
    )

    logging.info("Stopping the API service")


if __name__ == "__main__":
    main()
