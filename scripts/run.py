#!/usr/bin/env python3
import os
import sys
import logging
import subprocess

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/adme_dataset_download.log')),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Quick dependency check and installer."""
    required_packages = ['pytdc', 'pandas']
    
    for pkg in required_packages:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            logger.info(f"Installing missing package: {pkg}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', pkg])

def main():
    try:
        # Set up environment
        logger.info("Starting ADME dataset download process")
        setup_environment()
        
        # Import libraries
        import pandas as pd
        from tdc.single_pred import ADME
        
        # Configuration
        DATASET_NAME = 'BBB_Martins'
        OUTPUT_DIR = os.path.expanduser('~/research_data/adme_datasets')
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Download dataset
        logger.info(f"Downloading dataset: {DATASET_NAME}")
        adme_data = ADME(name=DATASET_NAME)
        full_dataset = adme_data.get_data()
        
        # Save full dataset
        full_path = os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_full.csv")
        full_dataset.to_csv(full_path, index=False)
        logger.info(f"Full dataset saved to: {full_path}")
        
        # Save splits
        splits = adme_data.get_split()
        for split_name, split_data in splits.items():
            split_path = os.path.join(OUTPUT_DIR, f"{DATASET_NAME}_{split_name}.csv")
            pd.DataFrame(split_data).to_csv(split_path, index=False)
            logger.info(f"Saved {split_name} split to: {split_path}")
        
        logger.info("Dataset download completed successfully")
    
    except Exception as e:
        logger.error(f"Error during dataset download: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()