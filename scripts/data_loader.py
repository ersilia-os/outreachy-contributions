from tdc.multi_pred import DrugRes
import os
import shutil 
import pandas as pd

class DataDownloader:
    def __init__(self, data_dir="../data", pickle_file="../data/gdsc1.pkl"):
        self.data_dir = os.path.abspath(data_dir)
        self.pickle_file = os.path.abspath(pickle_file)
        self.data = None
        self.gdsc_df = None
        self.benchmark_df = None
        self.gdsc_gene = None

    def fetch_gdsc1_dataset(self):
        """
        Downloads the GDSC1 dataset and moves it to the data folder.
        """
        try:
            print("Downloading dataset...")
            self.data = DrugRes(name="GDSC1")
            self.gdsc_df = self.data.get_data()

            # Ensure gdsc_gene_symbols.tab is created
            self.data.get_gene_symbols()
            self.gdsc_gene = pd.read_csv("../data/gdsc_gene_symbols.tab", sep="\t")  # Tab-separated file

            # Move the downloaded "data" folder to the target location
            downloaded_data_path = os.path.join(os.getcwd(), "data")

            # Remove old folder before replacing 
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)

            shutil.move(downloaded_data_path, self.data_dir)
            print(f"Dataset successfully moved to {self.data_dir}")

            return self.data, self.gdsc_df, self.gdsc_gene

        except Exception as e:
            print(f"Error: {e}")
            return None, None, None
    
    def load_benchmark(self):
        """
        Loads the benchmark dataset from a saved pickle file.
        """
        try:
            if not os.path.exists(self.pickle_file):
                raise FileNotFoundError(f"File not found: {self.pickle_file}")

            self.benchmark_df = pd.read_pickle(self.pickle_file)
            print(f"Dataset successfully loaded from {self.pickle_file}")
            return self.benchmark_df

        except FileNotFoundError as fnf_error:
            print(fnf_error)
            return None
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None