"""
Generate molecular features using RDKit's Morgan fingerprints.
This script converts SMILES strings to 2048-bit fingerprint vectors.
"""

import os
import json
import logging
from datetime import datetime
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from rdkit import Chem
from rdkit.Chem import AllChem


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/featurization.log'),
        logging.StreamHandler()
    ]
)

def setup_directories():
    """Create necessary directories if they don't exist."""
    dirs = ['data/features', 'data/processed', 'data/visualizations']
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def load_data(split_name):
    """Load data from a specific split and process permeability values.
    
    Converts log10 permeability (Y) to actual permeability in cm/s and creates
    binary labels using threshold of 8e-6 cm/s.
    """
    try:
        df = pd.read_csv(f'data/caco2_{split_name}.csv')
        
        # Convert log10 permeability to actual permeability in cm/s
        df['Permeability'] = np.power(10, df['Y'])
        
        # Create binary labels using industry-standard threshold
        threshold = 8e-6  # 8 × 10⁻⁶ cm/s
        df['Binary'] = (df['Permeability'] >= threshold).astype(int)
        
        return df
    except FileNotFoundError:
        logging.error(f"Could not find data file for {split_name} split")
        raise

def validate_features(features, split_name):
    """Validate generated features and compute statistics."""
    features = np.array(features)
    
    
    if len(features.shape) != 2:
        raise ValueError(f"Features should be 2D array, got shape {features.shape}")
    
    
    stats = {
        'split': split_name,
        'n_samples': features.shape[0],
        'n_features': features.shape[1],
        'mean': float(np.mean(features)),
        'std': float(np.std(features)),
        'min': float(np.min(features)),
        'max': float(np.max(features)),
        'n_zeros': int(np.sum(features == 0)),
        'n_nan': int(np.sum(np.isnan(features))),
        'n_inf': int(np.sum(np.isinf(features)))
    }
    
    
    logging.info(f"Feature statistics for {split_name}:")
    for k, v in stats.items():
        logging.info(f"  {k}: {v}")
    
    return stats

def visualize_features(features, labels, split_name):
    """Create PCA visualization of the features."""
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    
    pca = PCA(n_components=2)
    features_2d = pca.fit_transform(features_scaled)
    
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(features_2d[:, 0], features_2d[:, 1], 
                         c=labels, cmap='coolwarm', alpha=0.6)
    plt.colorbar(scatter, label='Permeability (Binary)')
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
    plt.title(f'PCA of Morgan Fingerprints - {split_name.capitalize()} Set')
    
    
    plt.savefig(f'data/visualizations/pca_features_{split_name}.png')
    plt.close()
    
    return pca.explained_variance_ratio_

def featurize_molecules(smiles_list, radius=3, nBits=2048):
    """Generate Morgan fingerprint features for a list of SMILES strings.

    Args:
        smiles_list: List of SMILES strings
        radius: Radius for Morgan fingerprints (default: 3)
        nBits: Number of bits in fingerprint (default: 2048)

    Returns:
        features: List of feature vectors
        failed_indices: List of indices where featurization failed
    """
    features = []
    failed_indices = []

    for idx, smiles in enumerate(tqdm(smiles_list, desc="Generating features")):
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError(f"Could not parse SMILES: {smiles}")
            
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits)
            
            features.append(np.array([int(b) for b in fp.ToBitString()]))
        except Exception as e:
            logging.warning(f"Error processing SMILES {smiles}: {str(e)}")
            failed_indices.append(idx)
            features.append(None)
    return features, failed_indices

def main():
    start_time = datetime.now()
    logging.info("Starting featurization process")
    
    
    setup_directories()
    
    
    logging.info("Starting Morgan fingerprint generation...")
    
    try:
        all_stats = []
        total_molecules = 0
        successful_molecules = 0
        
        
        for split in ['train', 'valid', 'test']:
            logging.info(f"\nProcessing {split} set...")
            
            
            df = load_data(split)
            total_molecules += len(df)
            
            
            features, failed_indices = featurize_molecules(df['Drug'].tolist())
            
            
            valid_indices = [i for i in range(len(features)) if i not in failed_indices]
            features = [features[i] for i in valid_indices]
            df = df.iloc[valid_indices].reset_index(drop=True)
            successful_molecules += len(valid_indices)
            
            
            stats = validate_features(features, split)
            all_stats.append(stats)
            
            
            var_explained = visualize_features(features, df['Binary'].values, split)
            logging.info(f"Total variance explained by 2 PCs: {sum(var_explained):.1%}")
            
            
            np.save(f'data/features/caco2_{split}_features.npy', np.array(features))
            df.to_csv(f'data/processed/caco2_{split}.csv', index=False)
            
            logging.info(f"Saved {len(features)} feature vectors for {split} set")
        
        
        with open('data/features/featurization_stats.json', 'w') as f:
            json.dump({
                'timestamp': start_time.isoformat(),
                'total_molecules': total_molecules,
                'successful_molecules': successful_molecules,
                'success_rate': successful_molecules / total_molecules,
                'splits': all_stats
            }, f, indent=2)
        
        logging.info("\nFeaturization completed successfully!")
        logging.info(f"Total time: {datetime.now() - start_time}")
        logging.info(f"Success rate: {successful_molecules}/{total_molecules} "
                    f"({successful_molecules/total_molecules:.1%})")
    
    finally:
        
        pass

if __name__ == "__main__":
    main()
