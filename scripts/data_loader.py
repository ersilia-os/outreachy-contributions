import os
import shutil
import pandas as pd
from tdc.multi_pred import TCREpitopeBinding

class DataDownloader:
    def __init__(self, data_dir = "../data"):
        self.data_dir = os.path.abspath(data_dir)
        self.data = None
        self.weber_df = None
        
    def fetch_weber_dataset(self):
        """
        Downloads the Weber TCR-Epitope dataset and saves it to the data folder.
        """
        try:
            # Check if data directory exists and delete it if needed
            if os.path.exists(self.data_dir):
                print(f"Removing existing data directory: {self.data_dir}")
                shutil.rmtree(self.data_dir)
                
            # Create the directory again
            os.makedirs(self.data_dir, exist_ok=True)
            
            print("Downloading Weber dataset...")
            # This will automatically download and save data to the specified path
            self.data = TCREpitopeBinding(name='weber', path=self.data_dir)
            
            # Get the data as a DataFrame
            self.weber_df = self.data.get_data()
            
            print(f"Dataset successfully downloaded to {self.data_dir}")
            print(f"DataFrame shape: {self.weber_df.shape}")
            
            return self.data, self.weber_df
            
        except Exception as e:
            print(f"Error: {e}")
            return None, None