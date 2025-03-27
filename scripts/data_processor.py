import os
import logging
import json
import time
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import pandas as pd

class DataProcessor:
    def __init__(self, input_csv, output_csv, log_dir="..data//logs/"):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.log_dir = os.path.abspath(log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

        # JSON log file
        self.log_file = os.path.join(self.log_dir, "data_processing_log.json")
        self.log_data = []

    def process_csv(self):
        """
        Reads a CSV file, fills missing Drug_IDs, and saves the processed data.
        """
        try:
            df = pd.read_csv(self.input_csv)
        except Exception as e:
            self.logger.error(f"Error reading CSV file: {e}")
            return

        if "Drug" not in df.columns or "Drug_ID" not in df.columns:
            self.logger.error("CSV must contain 'Drug' and 'Drug_ID' columns.")
            return

        missing_ids = df[df["Drug_ID"].isna()]
        if missing_ids.empty:
            self.logger.info("No missing Drug_IDs found. No processing needed.")
            return

        self.logger.info(f"Processing {len(missing_ids)} rows with missing Drug_IDs in {self.input_csv}...")

        for index, row in missing_ids.iterrows():
            smile = row["Drug"]
            mol = Chem.MolFromSmiles(smile)

            if mol:
                formula = rdMolDescriptors.CalcMolFormula(mol)
                try:
                    compounds = pcp.get_compounds(formula, 'formula')
                    if compounds:
                        name = compounds[0].synonyms[0] if compounds[0].synonyms else compounds[0].iupac_name
                        drug_id = name
                    else:
                        name = formula  # Fallback to formula
                        drug_id = formula

                    df.at[index, "Drug_ID"] = drug_id  

                    log_entry = {"SMILES": smile, "Formula": formula, "Name": name, "Drug_ID": drug_id}
                    self.logger.info(f"Processed: {log_entry}")
                except Exception as e:
                    self.logger.error(f"Error fetching data for {formula}: {e}")
                    df.at[index, "Drug_ID"] = formula  # Use formula as fallback

                    log_entry = {"SMILES": smile, "Formula": formula, "Error": str(e)}

                # Save log entry
                self.log_data.append(log_entry)

                # Pause to avoid API rate limits
                time.sleep(5)
            else:
                self.logger.error(f"Invalid SMILES: {smile}")
                self.log_data.append({"SMILES": smile, "Error": "Invalid SMILES"})

        df.to_csv(self.output_csv, index=False)
        self.logger.info(f"Processed data saved to {self.output_csv}")

        with open(self.log_file, "w") as f:
            json.dump(self.log_data, f, indent=4)

        self.logger.info("Processing complete! Logs saved to: " + self.log_file)
