import os
import time
import pandas as pd
import logging
import subprocess

# Correct model identifier
ERSILIA_DESCRIPTORS = "eos8a4x"

class FeatureExtractor:
    def __init__(self, log_file="ersilia_output.log"):
        """
        Initializes the FeatureExtractor for train, valid, and test datasets.
        Automatically manages input and output file paths.
        """
        self.datasets = {
            "train": {"input": "data/bbb_train.csv", "output": "data/bbb_train_features.csv"},
            "valid": {"input": "data/bbb_valid.csv", "output": "data/bbb_valid_features.csv"},
            "test": {"input": "data/bbb_test.csv", "output": "data/bbb_test_features.csv"},
        }
        self.log_file = log_file

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def run_command(self, command):
        """Run a shell command and capture its output."""
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            self.logger.info(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {command}")
            self.logger.error(e.stderr)
            return None

    def generate_features(self):
        """Extracts features for train, valid, and test datasets using Ersilia CLI."""
        try:
            # Fetch model if not already available
            self.logger.info(" Fetching RDKit descriptors model from Ersilia...")
            fetch_output = self.run_command(f"ersilia -v fetch {ERSILIA_DESCRIPTORS}")
            if fetch_output is None:
                self.logger.error(" Failed to fetch the model.")
                return None

            # Serve the model
            self.logger.info(" Serving the model in the background...")
            serve_output = self.run_command(f"ersilia -v serve {ERSILIA_DESCRIPTORS}")
            if serve_output is None:
                self.logger.error(" Failed to serve the model.")
                return None

            # Reduce wait time while ensuring the model is running
            self.logger.info(" Waiting 20 seconds for the model to fully start...")
            time.sleep(20)

            for dataset, paths in self.datasets.items():
                input_file = paths["input"]
                output_file = paths["output"]

                if not os.path.exists(input_file):
                    self.logger.error(f" Dataset not found: {input_file}")
                    continue

                self.logger.info(f" Running feature extraction for {dataset} dataset...")
                run_command = f"ersilia -v run -i {input_file} -o data/{dataset}_descriptors.csv"
                run_output = self.run_command(run_command)

                if run_output is None:
                    self.logger.error(f" Feature extraction failed for {dataset}.")
                    continue

                #  Verify if extraction was successful
                descriptors_file = f"data/{dataset}_descriptors.csv"
                if not os.path.exists(descriptors_file):
                    self.logger.error(f" Feature extraction failed for {dataset}! Check Ersilia logs.")
                    continue

                #  Merge extracted features with the original dataset
                self.logger.info(f" Merging extracted features with the {dataset} dataset...")
                descriptors = pd.read_csv(descriptors_file)
                df = pd.read_csv(input_file)

                # Remove duplicate SMILES column (if exists) and merge
                df = pd.concat([df, descriptors.drop(columns=["SMILES"], errors='ignore')], axis=1)
                df.to_csv(output_file, index=False)

                self.logger.info(f" Feature extraction complete! Data saved to {output_file}")

        except Exception as e:
            self.logger.error(f" Error during feature extraction: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    extractor = FeatureExtractor()
    extractor.generate_features()
