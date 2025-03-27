import pandas as pd
import os
from glob import glob
from data_loader import DataDownloader
from explore import ExploratoryDataAnalysis
from data_processor import DataProcessor
from featurize import Featurizer

name = input("Model name: ")
print("Starting Automation...")

# Step 1: Download Data
download = input("Use Existing Data? (Y/N): ").strip().upper()

if download == 'N':
    print("\nDownloading data...")
    downloader = DataDownloader()
    df, splits = downloader.fetch_dataset(name=name)
else:
    print("\nLoading existing data...")
    try:
        df = pd.read_csv(f'../data/{name}/{name}.csv')
        train = pd.read_csv(f'../data/{name}/train.csv') 
        validation = pd.read_csv(f'../data/{name}/validation.csv') 
        test = pd.read_csv(f'../data/{name}/test.csv') 
        splits = {"train": train, "validation": validation, "test": test}
        print("Data successfully loaded.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Dataset not found, attempting to download...")
        downloader = DataDownloader()
        df, splits = downloader.fetch_dataset(name=name)


# Step 2: Data Preprocessing
print("\nPerforming Preprocessing...")
files_to_preprocess = [f"../data/{name}/{key}.csv" for key in splits.keys()]
for file in files_to_preprocess:
    processor = DataProcessor(input_csv = file, output_csv = file)
    processor.process_csv()


# Step 3: Perform EDA
print("\nPerforming EDA...")
eda = ExploratoryDataAnalysis(model_name = name)
eda.generate_eda()

# Step 4: Perform Featurisation
count = len(glob(f"../data/{name}/*eos24ci_featurized*"))
print("\nPerforming Featurisation...")
if count == 0:
    featurizer = Featurizer(model_id = "eos24ci")
    files = ['train', 'test', 'validation']
    for file in files:
        output_path = featurizer.featurize(input_file = file, dataset_name = name)

else:
    print("\nData has already by Featurised...")

# More Steps to be added

print("\nAutomation complete! All results are saved.")