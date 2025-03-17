import os
import logging
from dotenv import load_dotenv
from config.settings import ConfigParms as sc
from dp_app import dp_app_core as dpc
from utils import logger as ufl

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

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.app_log_dir}/{script_name}.log")
    logging.info("Configs are set")

    logging.info("Starting the API service")

    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        log_config=f"{sc.app_config_dir}/api_log.ini",
    )

    logging.info("Stopping the API service")


if __name__ == "__main__":
    main()
