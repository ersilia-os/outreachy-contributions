import os
import time
import logging
import pandas as pd
import subprocess
from eda import ExploratoryDataAnalysis
from featurise import FeatureExtractor
from data_loader import Dataloader

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# File paths
DATA_PATH = "data/bbb.csv"
FEATURES_PATH = "data/bbb_features.csv"

def main():
    """Automates the entire BBB dataset processing pipeline."""

    # Step 1: Download dataset if not present
    if not os.path.exists(DATA_PATH):
        logger.info("📥 Dataset not found. Downloading now...")
        downloader = Dataloader()
        downloader.download_data()
    else:
        logger.info("✅ Dataset found. Skipping download.")

    # Step 2: Perform Exploratory Data Analysis
    logger.info("📊 Running Exploratory Data Analysis...")
    eda = ExploratoryDataAnalysis()
    eda.generate_visuals()

    # Step 3: Extract Features using Ersilia CLI
    if not os.path.exists(FEATURES_PATH):
        logger.info("🔬 Extracting molecular descriptors...")
        extractor = FeatureExtractor()
        extractor.generate_features()
    else:
        logger.info("✅ Feature extraction already done. Skipping.")

    logger.info("🚀 Pipeline completed successfully!")

if __name__ == "__main__":
    main()