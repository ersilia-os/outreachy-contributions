import os

print("Starting automation...")

# Step 1: Download Data
print("\nDownloading data...")
os.system("python data_loader.py")

# Step 2: Perform EDA
print("\nPerforming EDA...")
os.system("python eda.py")

# More Steps to be added

print("\nAutomation complete! All results are saved.")