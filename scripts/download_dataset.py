from tdc.single_pred import ADME
import pandas as pd
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Load Caco2 permeability dataset (binary classification)
data = ADME(name='Caco2_Wang')

# Split into train/valid/test sets using default split
split = data.get_split()

# Save splits to CSV files
split['train'].to_csv('data/caco2_train.csv', index=False)
split['valid'].to_csv('data/caco2_valid.csv', index=False)
split['test'].to_csv('data/caco2_test.csv', index=False)

print("Dataset downloaded and saved to data directory!")
print(f"Training set size: {len(split['train'])} samples")
print(f"Validation set size: {len(split['valid'])} samples")
print(f"Test set size: {len(split['test'])} samples")
