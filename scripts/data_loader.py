import os
import shutil
import logging
import pandas as pd
from tdc.multi_pred import TCREpitopeBinding

class DataDownloader:
    def __init__(self, data_dir="../data"):
        self.data_dir = os.path.abspath(data_dir)
        self.data_file = os.path.join(self.data_dir, "weber.csv")  # Save dataset here
        self.data = None
        self.weber_df = None

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def fetch_weber_dataset(self):
        """
        Downloads the Weber TCR-Epitope dataset, saves it as a CSV file, and returns the DataFrame.
        """
        try:
            # Ensure clean data directory
            if os.path.exists(self.data_dir):
                self.logger.info(f"Removing existing data directory: {self.data_dir}")
                shutil.rmtree(self.data_dir)
                
            os.makedirs(self.data_dir, exist_ok=True)
            
            self.logger.info("Downloading Weber dataset...")
            self.data = TCREpitopeBinding(name='weber', path=self.data_dir)
            self.weber_df = self.data.get_data()
            
            # Save dataset as CSV
            self.weber_df.to_csv(self.data_file, index=False)
            self.logger.info(f"Dataset saved to {self.data_file} (Shape: {self.weber_df.shape})")
            
            return self.data, self.weber_df
        except Exception as e:
            self.logger.error(f"Error: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    downloader = DataDownloader()
    downloader.fetch_weber_dataset()