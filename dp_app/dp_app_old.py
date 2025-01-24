from dp_app import settings as sc

import os
import argparse
import logging

from dp_app import dp_app_core as dpc
from utils import logger as ufl


def main():
    parser = argparse.ArgumentParser(description="Data Profiling Application")
    parser.add_argument(
        "-e", "--env", help="Environment", const="dev", nargs="?", default="dev"
    )
    parser.add_argument(
        "-d",
        "--dataset_id",
        help="Source data",
        const="1",
        nargs="?",
        default="1",
        required=True,
    )

    # Sample invocation
    # python dp_app.py --env='dev' --dataset_id='3'

    script_name = os.path.splitext(os.path.basename(__file__))[0]

    logging.info("Starting %s", script_name)

    # Get the arguments
    args = vars(parser.parse_args())
    logging.info(args)
    env = args["env"]
    src_dataset_id = args["dataset_id"]

    cfg = sc.load_config(env)
    sc.set_config(cfg)
    # print(sc.source_file_path)

    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")
    logging.info(cfg)

    dp_results = dpc.apply_ner_model(dataset_id=src_dataset_id)

    logging.debug("Data profiling results for dataset %s", src_dataset_id)
    logging.debug(dp_results)

    logging.info("Finishing %s", script_name)


if __name__ == "__main__":
    main()
