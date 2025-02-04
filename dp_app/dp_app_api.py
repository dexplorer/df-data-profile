from dp_app import settings as sc
from dp_app import dp_app_core as dpc
import logging

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
async def profile_dataset(dataset_id: str, env: str = "dev", cycle_date: str = ""):
    """
    Profile the dataset.
    """

    sc.load_config(env)

    logging.info("Configs are set")

    logging.info("Start profiling the dataset %s", dataset_id)
    dp_results = dpc.apply_ner_model(dataset_id=dataset_id, cycle_date=cycle_date)

    logging.info("Finished profiling the dataset %s", dataset_id)

    return {"results": dp_results}


if __name__ == "__main__":
    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        log_config=f"{sc.APP_ROOT_DIR}/cfg/api_log.ini",
    )
