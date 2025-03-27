import os
import logging
import pandas as pd
from tdc.single_pred import Tox

class DataDownloader:
    VALID_DATASETS = {"hERG", "hERG_Karim", "AMES", "DILI", "Skin Reaction", "LD50_Zhu", "Carcinogens_Lagunin", "ClinTox"}

    def __init__(self, data_dir = "../data/"):
        self.data_dir = os.path.abspath(data_dir)

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def fetch_dataset(self, name, method="scaffold"):
        """
        Downloads the specified dataset, applies splitting, saves all splits as CSV, and returns the DataFrame.
        
        Args:
        - name (str): Name of the dataset (must be in VALID_DATASETS).
        - method (str): Splitting method ('random' or 'scaffold').
        
        Returns:
        - df (pd.DataFrame): The full dataset DataFrame.
        - splits (dict): Dictionary containing train, validation, and test DataFrames.
        """
        try:
            if name not in self.VALID_DATASETS:
                self.logger.error(f"Invalid dataset name '{name}'. Allowed names: {self.VALID_DATASETS}")
                return None, None, None

            if method not in ["random", "scaffold"]:
                self.logger.error(f"Invalid split method '{method}'. Choose 'random' or 'scaffold'.")
                return None, None, None

            # Set dataset directory inside data_dir
            dataset_dir = os.path.join(self.data_dir, name)
            dataset_file = os.path.join(dataset_dir, f"{name}.csv")

            os.makedirs(dataset_dir, exist_ok=True)

            if os.path.exists(dataset_file):
                self.logger.info(f"Deleting existing dataset file: {dataset_file}")
                os.remove(dataset_file)

            self.logger.info(f"Downloading '{name}' dataset...")
            data = Tox(name=name, path=dataset_dir)
            df = data.get_data()

            df.to_csv(dataset_file, index=False)
            self.logger.info(f"Dataset '{name}' saved to {dataset_file} (Shape: {df.shape})")

            self.logger.info(f"Splitting dataset using '{method}' method...")
            splits = data.get_split(method=method)

            train = pd.DataFrame(splits["train"])
            validation = pd.DataFrame(splits["valid"])
            test = pd.DataFrame(splits["test"])

            train.to_csv(os.path.join(dataset_dir, "train.csv"), index=False)
            validation.to_csv(os.path.join(dataset_dir, "validation.csv"), index=False)
            test.to_csv(os.path.join(dataset_dir, "test.csv"), index=False)

            # Log split details
            self.logger.info(f"Train set saved (Shape: {train.shape})")
            self.logger.info(f"Validation set saved (Shape: {validation.shape})")
            self.logger.info(f"Test set saved (Shape: {test.shape})")

            return df, {"train": train, "validation": validation, "test": test}
            
        except Exception as e:
            self.logger.error(f"Error downloading '{name}': {e}", exc_info=True)
            return None, None