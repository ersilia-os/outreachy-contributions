from tdc.benchmark_group import admet_group
from sklearn.model_selection import train_test_split
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

# Load dataset
group = admet_group(path="data/")
benchmark = group.get("ames")

# Use the provided split
train_val = benchmark["train_val"]
test = benchmark["test"]

# Manually split train_val into train/val (85/15 of train_val)
train, val = train_test_split(train_val, test_size=0.15, stratify=train_val["Y"], random_state=42)

# Save to CSV
train.to_csv("data/ames_train.csv", index=False)
val.to_csv("data/ames_val.csv", index=False)
test.to_csv("data/ames_test.csv", index=False)

print("✅ Ames dataset successfully split and saved!")
print(train.head())
