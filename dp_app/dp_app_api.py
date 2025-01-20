from dp_app import settings as sc
from dp_app import dp_app_core as dpc
from utils import logger as ufl
import logging
import os

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    """
    Default route
    """

    return {"message": "Data Profiling App"}


@app.get("/profile-dataset/{dataset_id}")
async def profile_dataset(dataset_id: str, env: str = "dev"):
    """
    profile the dataset.
    See ./log/dp_app_cli.log for logs.
    """

    cfg = sc.load_config(env)
    sc.set_config(cfg)

    # script_name = os.path.splitext(os.path.basename(__file__))[0]
    # ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info(f"Configs are set")

    logging.info(f"Start profiling the dataset {dataset_id}")
    dp_results = dpc.apply_ner_model(dataset_id=dataset_id)

    logging.info(f"Finished profiling the dataset {dataset_id}")

    return {"results": dp_results}


if __name__ == "__main__":
    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        log_config=f"{sc.APP_ROOT_DIR}/cfg/dp_app_api_log.ini",
    )
