from dp_app import settings as sc

import os
import argparse
import logging

from dp_app import dp_app_core as dpc
from dp_app.utils import logger as ufl


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

    logging.info(f"Starting {script_name}")

    # Get the arguments
    args = vars(parser.parse_args())
    logging.info(args)
    env = args["env"]
    src_dataset_id = args["dataset_id"]

    logging.info(f"Set configs")
    cfg = sc.load_config(env)
    sc.set_config(cfg)
    # print(sc.source_file_path)
    logging.info(cfg)

    dp_results = dpc.apply_ner_model(dataset_id=src_dataset_id)

    print(f"Data profiling results for dataset {src_dataset_id}")
    print(dp_results)

    logging.info(f"Finishing {script_name}")


if __name__ == "__main__":
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_name=script_name)
    main()
