import pandas as pd
import torch
from pathlib import Path
from eosce.models import ErsiliaCompoundEmbeddings
from dataloader import get_dataloader  # Importing the existing dataloader script

def featurize_and_save(data_path, output_path, batch_size=32):
    # Load data using the existing DataLoader
    train_loader, valid_loader, test_loader = get_dataloader(data_path, batch_size=batch_size)
    
    # Initialize Ersilia's compound embedding model
    model = ErsiliaCompoundEmbeddings()
    
    # Function to featurize a batch of SMILES
    def featurize_batch(batch):
        smiles, labels = zip(*batch)  # Extract SMILES and labels
        embeddings = model.transform(list(smiles))  # Compute embeddings
        return embeddings, labels
    
    all_embeddings, all_labels = [], []
    
    # Process each batch from the train, validation, and test loaders
    for loader in [train_loader, valid_loader, test_loader]:
        for batch in loader:
            embeddings, labels = featurize_batch(batch)
            all_embeddings.extend(embeddings)
            all_labels.extend(labels)
    
    # Convert to DataFrame and save
    df = pd.DataFrame({"embedding": all_embeddings, "label": all_labels})
    df.to_parquet(output_path)
    
    print(f"✅ Featurized data saved to {output_path}")

if __name__ == "__main__":
    data_path = "../data/Single/tox21_NR-AR.parquet"  # Adjust as needed
    output_path = "../output/tox21_NR-AR_featurized.parquet"
    featurize_and_save(data_path, output_path)
