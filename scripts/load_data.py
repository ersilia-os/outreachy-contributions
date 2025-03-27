import logging, os
from typing import List
from dotenv import load_dotenv
from pathlib import Path
from tdc.single_pred import HTS

# load env variables to run script
load_dotenv()

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

if not (LOCAL_DATA_PATH := os.environ.get("LOCAL_DATA_PATH")):
    raise ValueError("LOCAL_DATA_PATH environment variable is not set.")

if not (HTS_DATASET_NAME := os.environ.get("HTS_DATASET_NAME")):
    raise ValueError("HTS_DATASET_NAME is not set.")


def load_tdc_hts_data(
    dataset_name: str,
    data_store_path: Path,
    radom_split: bool = False,
    print_dataset_stats=True,
) -> List:
    """Utility to retrieve TDC HTS single instance prediction data based on the specified dataset
        and splits the data to the default ratio of [0.7, 0.1, 0.2] for train/val/test

        for more datails visit:
        https://tdcommons.ai/single_pred_tasks/hts

    Args:
        dataset_name (str): name of dataset from the TDC HTS single instance prediction problem \n
        data_store_path (Path): local directory path to store loaded dataset \n
        radom_split (bool, optional): Option to split the data using random split or scaffold method. Defaults False \n
        print_dataset_stats (bool, optional): Option to display basic dataset statictics after loading. Defaults to True. \n
    """
    try:
        logging.info(f"started loading dataset {dataset_name}...")
        # init HTS class to load data based on specified  params
        data = HTS(
            name=dataset_name, path=data_store_path, print_stats=print_dataset_stats
        )
        # select type of splict specific to HTS single-instance prediction data
        split_type = "random" if radom_split else "scaffold"
        split = data.get_split(method=split_type)

        # save splits to data directory
        os.makedirs(data_store_path, exist_ok=True)
        for name, df in split.items():
            df.to_csv(
                os.path.join(data_store_path, f"{dataset_name}_{name}.csv".lower()),
                index=False,
            )

        logging.info(
            f"Loaded dataset {dataset_name} with {split_type} split as CSV into {os.path.abspath(data_store_path)} 🚀"
        )
    except Exception as e:
        logging.error(f"could not load dataset ⚠️ --> {e}")


if __name__ == "__main__":
    load_tdc_hts_data(
        dataset_name=HTS_DATASET_NAME, data_store_path=Path(LOCAL_DATA_PATH + "/raw")
    )
