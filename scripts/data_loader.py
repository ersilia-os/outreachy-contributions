import os
import shutil
import logging
import pandas as pd
from tdc.single_pred import ADME

class Dataloader:
    def __init__(self, data_dir="data/"):
        self.data_dir = os.path.abspath(data_dir)
        self.data_file = os.path.join(self.data_dir, "bbb.csv")  # Save BBB dataset here
        self.train_file = os.path.join(self.data_dir, "bbb_train.csv")
        self.valid_file = os.path.join(self.data_dir, "bbb_valid.csv")
        self.test_file = os.path.join(self.data_dir, "bbb_test.csv")
        
        self.data = None
        self.bbb_df = None

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def fetch_bbb_dataset(self):
        """
        Downloads the BBB (Blood-Brain Barrier) dataset from the ADME Pharmacokinetics category.
        Saves it as a CSV file and returns the DataFrame.
        """
        try:
            # Ensure clean data directory
            if os.path.exists(self.data_dir):
                self.logger.info(f"Removing existing data directory: {self.data_dir}")
                shutil.rmtree(self.data_dir)

            os.makedirs(self.data_dir, exist_ok=True)

            self.logger.info("Downloading BBB dataset from ADME Pharmacokinetics...")
            self.data = ADME(name="BBB_Martins", path=self.data_dir)
            self.bbb_df = self.data.get_data()

            # Save full dataset
            self.bbb_df.to_csv(self.data_file, index=False)
            self.logger.info(f"✅ Full dataset saved to {self.data_file} (Shape: {self.bbb_df.shape})")

            # Get train, validation, and test splits
            split = self.data.get_split()
            
            train_df = split["train"]
            valid_df = split["valid"]
            test_df = split["test"]

            # Save each split as a CSV file
            train_df.to_csv(self.train_file, index=False)
            valid_df.to_csv(self.valid_file, index=False)
            test_df.to_csv(self.test_file, index=False)

            self.logger.info(f"✅ Train set saved to {self.train_file} (Shape: {train_df.shape})")
            self.logger.info(f"✅ Validation set saved to {self.valid_file} (Shape: {valid_df.shape})")
            self.logger.info(f"✅ Test set saved to {self.test_file} (Shape: {test_df.shape})")

            return self.data, self.bbb_df, split
        except Exception as e:
            self.logger.error(f"❌ Error: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    downloader = Dataloader()
    downloader.fetch_bbb_dataset()
