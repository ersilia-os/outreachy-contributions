import os
import pandas as pd
import seaborn as sns
import logging
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # This is correct for non-interactive backends
import matplotlib.pyplot as plt

class ExploratoryDataAnalysis:
    def __init__(self, model_name, data_dir = "../data/", figure_base_dir = "../data/figures/"):
        self.model_name = model_name
        self.data_path = os.path.join(data_dir, model_name, f"{model_name}.csv")
        self.figure_dir = os.path.join(figure_base_dir, model_name)  # Ensuring model-specific directory

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

        self.logger.info(f"Absolute data path: {os.path.abspath(self.data_path)}")
        self.logger.info(f"Absolute figure directory: {os.path.abspath(self.figure_dir)}")

    def generate_eda(self):
        """
        Generates and saves EDA visualizations if the dataset exists.
        """
        try:
            if not os.path.abspath(self.data_path):
                self.logger.error(f"Dataset not found: {self.data_path}")
                return None

            
            df = pd.read_csv(self.data_path)

            os.makedirs(self.figure_dir, exist_ok=True)
            self.logger.info(f"Figure directory verified at: {os.path.abspath(self.figure_dir)}")

            # 1. Label Distribution
            if "Y" in df.columns:
                counts = dict(df.Y.value_counts()).items()
                for key, value in counts:
                    if self.model_name == 'hERG':
                        classification = "blockers" if key == 1.0 else "non-blockers"
                    else:
                        classification = "mutagens" if key == 1.0 else "non-mutagens"
                    self.logger.info(f"{value} drugs are classified as {classification}")

                
                plt.figure(figsize=(10, 5))
                sns.barplot(x=df.Y.value_counts().index, y=df.Y.value_counts().values)
                plt.xlabel("Labels")
                plt.ylabel("Count")
                plt.title("Label Distribution")
                plt.show()

                fig_path = os.path.join(self.figure_dir, "label_distribution.png")
                plt.savefig(fig_path)
                self.logger.info(f"Saved figure to: {os.path.abspath(fig_path)}")
                plt.close()
            else:
                self.logger.warning(f"Column 'Y' not found in {self.data_path}")

            # 2. SMILES Length Distribution
            if "Drug" in df.columns:
                plt.figure(figsize=(10, 5))
                smiles_length = df['Drug'].str.len()
                sns.histplot(smiles_length, bins=20, kde=True)
                plt.title("SMILES Length Distribution")

                fig_path = os.path.join(self.figure_dir, "smiles_length.png")
                plt.savefig(fig_path)
                self.logger.info(f"Saved figure to: {os.path.abspath(fig_path)}")
                plt.close()
            else:
                self.logger.warning(f"Column 'Drug' not found in {self.data_path}")

            
            self.logger.info(f"EDA for {self.model_name} completed successfully.")

        except Exception as e:
            self.logger.error(f"Error during EDA: {e}", exc_info=True)
            return None