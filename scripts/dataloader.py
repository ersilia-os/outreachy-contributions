import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from sklearn.model_selection import train_test_split

class Tox21Dataset(Dataset):
    def __init__(self, data):
        self.smiles = data['Drug']
        self.labels = data['Y'].values.astype(float)
    
    def __len__(self):
        return len(self.smiles)
    
    def __getitem__(self, idx):
        return self.smiles.iloc[idx], torch.tensor(self.labels[idx], dtype=torch.float32)

def get_dataloader(data_path, batch_size=32, shuffle=True, train_frac=0.7, val_frac=0.1, test_frac=0.2, seed=42):
    # Load data
    df = pd.read_parquet(data_path)
    
    # Train-validation-test split
    train_data, temp_data = train_test_split(df, test_size=(1 - train_frac), random_state=seed, stratify=df['Y'])
    valid_data, test_data = train_test_split(temp_data, test_size=(test_frac / (test_frac + val_frac)), random_state=seed, stratify=temp_data['Y'])
    
    # Create datasets
    train_dataset = Tox21Dataset(train_data)
    valid_dataset = Tox21Dataset(valid_data)
    test_dataset = Tox21Dataset(test_data)
    
    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)
    valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, valid_loader, test_loader


# train_loader, valid_loader, test_loader = get_dataloader("../data/Single/tox21_NR-AR.parquet")
