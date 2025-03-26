import os
from data_loader import DataDownloader
from explore import ExploratoryDataAnalysis


name = input("Model name: ")
print("Starting automation...")

# Step 1: Download Data
downloader = DataDownloader()
data, df, splits = downloader.fetch_dataset(name = name)

print("\nDownloading data...")
os.system("python data_loader.py")

# Step 2: Perform EDA
print("\nPerforming EDA...")
eda = ExploratoryDataAnalysis(model_name = name)
eda.generate_eda()
os.system("python explore.py")

# More Steps to be added

print("\nAutomation complete! All results are saved.")