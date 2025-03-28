"""
Generate molecular features using Ersilia's Uni-Mol representation model (eos39co).
This script converts SMILES strings to feature vectors using the pre-trained Uni-Mol model.
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
from ersilia import ErsiliaModel

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/featurization_unimol.log'),
        logging.StreamHandler()
    ]
)

def setup_directories():
    """Create necessary directories if they don't exist."""
    dirs = [
        'data/features_unimol',
        'data/processed',
        'data/visualizations_unimol'
    ]
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
    """Validate generated features and compute statistics.
    
    Args:
        features: List or array of feature vectors
        split_name: Name of the data split (e.g., 'train', 'test')
        
    Returns:
        dict: Statistics about the features
        
    Raises:
        ValueError: If features are invalid or contain too many problematic values
    """
    if not features:
        raise ValueError(f"No valid features found for {split_name} split")
    
    # Convert list of features to numpy array
    try:
        features = np.array(features)
        logging.info(f"Initial features shape: {features.shape}")
    except Exception as e:
        logging.error(f"Error converting features to array: {str(e)}")
        raise ValueError(f"Features must be convertible to numpy array: {str(e)}")
    
    # Handle case where features is 1D array of embeddings
    if len(features.shape) == 1:
        logging.info(f"Got 1D array, first element type: {type(features[0])}")
        if hasattr(features[0], '__len__'):
            try:
                features = np.vstack(features)
                logging.info(f"Stacked features shape: {features.shape}")
            except Exception as e:
                logging.error(f"Error stacking features: {str(e)}")
                raise ValueError(f"Failed to stack 1D array into 2D matrix: {str(e)}")
        else:
            raise ValueError(f"Features must be a list of vectors, got scalar values")
    
    # Check for invalid values
    n_nan = int(np.sum(np.isnan(features)))
    n_inf = int(np.sum(np.isinf(features)))
    n_zeros = int(np.sum(features == 0))
    total_elements = features.size
    
    # Compute percentages
    pct_nan = (n_nan / total_elements) * 100
    pct_inf = (n_inf / total_elements) * 100
    pct_zeros = (n_zeros / total_elements) * 100
    
    # Check for concerning patterns
    if pct_nan > 1:  # More than 1% NaN values
        raise ValueError(f"Features contain {pct_nan:.2f}% NaN values, which is too high")
    if pct_inf > 1:  # More than 1% infinite values
        raise ValueError(f"Features contain {pct_inf:.2f}% infinite values, which is too high")
    if pct_zeros > 95:  # More than 95% zeros
        raise ValueError(f"Features contain {pct_zeros:.2f}% zero values, suggesting potential issues")
    
    # Compute detailed statistics
    stats = {
        'split': split_name,
        'n_samples': features.shape[0],
        'n_features': features.shape[1] if len(features.shape) > 1 else 1,
        'mean': float(np.mean(features)),
        'std': float(np.std(features)),
        'min': float(np.min(features)),
        'max': float(np.max(features)),
        'n_zeros': n_zeros,
        'pct_zeros': pct_zeros,
        'n_nan': n_nan,
        'pct_nan': pct_nan,
        'n_inf': n_inf,
        'pct_inf': pct_inf,
        'sparsity': float(n_zeros / total_elements)
    }
    
    logging.info(f"Feature statistics for {split_name}:")
    for k, v in stats.items():
        if isinstance(v, float):
            logging.info(f"  {k}: {v:.4f}")
        else:
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
    plt.title(f'PCA of Uni-Mol Features - {split_name.capitalize()} Set')
    
    plt.savefig(f'data/visualizations_unimol/pca_features_{split_name}.png')
    plt.close()
    
    return pca.explained_variance_ratio_

def featurize_molecules(smiles_list):
    """Generate Uni-Mol features for a list of SMILES strings.

    Args:
        smiles_list: List of SMILES strings

    Returns:
        features: List of feature vectors
        failed_indices: List of indices where featurization failed
    """
    if not smiles_list:
        logging.error("Empty SMILES list provided")
        return np.array([]), []

    features = []
    failed_indices = []
    expected_dim = None

    try:
        # Initialize Ersilia model
        model = ErsiliaModel("eos39co")
        model.serve()

        # Process molecules in batches to avoid memory issues
        batch_size = 32
        for i in tqdm(range(0, len(smiles_list), batch_size), desc="Generating features"):
            batch = smiles_list[i:i + batch_size]
            try:
                # Get embeddings for the batch using the run API
                result = model.run(batch)
                
                # Convert generator to list if necessary
                if hasattr(result, '__iter__') and not isinstance(result, (list, tuple)):
                    result = list(result)
                
                # Handle different types of results
                batch_embeddings = []
                
                if isinstance(result, (list, tuple)):
                    for idx, r in enumerate(result):
                        try:
                            # Extract embedding from output->outcome field
                            if isinstance(r, dict):
                                # Try different possible paths to get embeddings
                                embedding = None
                                if 'output' in r and 'outcome' in r['output']:
                                    embedding = r['output']['outcome']
                                elif 'outcome' in r:
                                    embedding = r['outcome']
                                elif 'output' in r:
                                    embedding = r['output']
                                
                                if embedding is not None and isinstance(embedding, (list, np.ndarray)):
                                    embedding_array = np.array(embedding)
                                    if embedding_array.size > 0:
                                        # Validate embedding dimensions
                                        if expected_dim is None:
                                            expected_dim = embedding_array.shape
                                        if embedding_array.shape == expected_dim:
                                            batch_embeddings.append(embedding_array)
                                        else:
                                            logging.warning(f"Inconsistent embedding dimensions at index {i + idx}. Expected {expected_dim}, got {embedding_array.shape}")
                                            failed_indices.append(i + idx)
                                    else:
                                        logging.warning(f"Empty embedding array at index {i + idx}")
                                        failed_indices.append(i + idx)
                                else:
                                    logging.warning(f"Invalid embedding format at index {i + idx}")
                                    failed_indices.append(i + idx)
                            else:
                                logging.warning(f"Invalid result format at index {i + idx}")
                                failed_indices.append(i + idx)
                        except Exception as e:
                            logging.warning(f"Error processing molecule {i + idx}: {str(e)}")
                            failed_indices.append(i + idx)
                
                if batch_embeddings:
                    features.extend(batch_embeddings)
                    logging.info(f"Processed batch {i}, got {len(batch_embeddings)} embeddings with shape {batch_embeddings[0].shape}")
                else:
                    logging.warning(f"No valid embeddings found in batch {i}")
                    failed_indices.extend(range(i, min(i + batch_size, len(smiles_list))))

            except Exception as e:
                logging.warning(f"Error processing batch {i}: {str(e)}")
                failed_indices.extend(range(i, min(i + batch_size, len(smiles_list))))

    except Exception as e:
        logging.error(f"Error initializing Uni-Mol model: {str(e)}")
        raise
    finally:
        try:
            model.clear()
        except:
            pass

    # Convert features to numpy array
    if features:
        try:
            features_array = np.array(features)
            logging.info(f"Final features shape: {features_array.shape}")
            return features_array, failed_indices
        except Exception as e:
            logging.error(f"Error converting features to array: {str(e)}")
    
    logging.error("No valid features found")
    return np.array([]), failed_indices

def main():
    start_time = datetime.now()
    logging.info("Starting featurization process")
    
    setup_directories()
    
    logging.info("Starting Uni-Mol feature generation...")
    
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
            
            np.save(f'data/features_unimol/caco2_{split}_features.npy', np.array(features))
            df.to_csv(f'data/processed/caco2_{split}_unimol.csv', index=False)
            
            logging.info(f"Saved {len(features)} feature vectors for {split} set")
        
        with open('data/features_unimol/featurization_stats.json', 'w') as f:
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
