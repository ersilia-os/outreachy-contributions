import os
import shutil
import logging
import pandas as pd
from tdc.single_pred import Tox

class DataDownloader:
    def __init__(self, data_dir="data/"):
        self.data_dir = os.path.abspath(data_dir)
        self.data_file = os.path.join(self.data_dir, "herg.csv")  # Save dataset here
        self.data = None
        self.herg_df = None

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def fetch_herg_dataset(self):
        """
        Downloads the herg hERG blockers dataset, saves it as a CSV file, and returns the DataFrame.
        """
        try:
            # Ensure clean data directory
            if os.path.exists(self.data_dir):
                self.logger.info(f"Removing existing data directory: {self.data_dir}")
                shutil.rmtree(self.data_dir)
                
            os.makedirs(self.data_dir, exist_ok=True)
            
            self.logger.info("Downloading herg dataset...")
            self.data = data = Tox(name = 'hERG', path = self.data_dir)
            self.herg_df = self.data.get_data()
            
            # Save dataset as CSV
            self.herg_df.to_csv(self.data_file, index=False)
            self.logger.info(f"Dataset saved to {self.data_file} (Shape: {self.herg_df.shape})")
            
            return self.data, self.herg_df
        except Exception as e:
            self.logger.error(f"Error: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    downloader = DataDownloader()
    downloader.fetch_herg_dataset()