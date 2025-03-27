import os
import pandas as pd
import seaborn as sns
import logging
from rdkit import Chem
from rdkit.Chem import Draw
import matplotlib.pyplot as plt

class ExploratoryDataAnalysis:
    def __init__(self, data_path="data/bbb.csv", figure_dir="figures/"):
        self.data_path = data_path
        self.figure_dir = figure_dir

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def generate_visuals(self):
        """
        Generates and saves three key EDA visualizations:
        1. Label Distribution (Does the drug cross the BBB?)
        2. SMILES String Length Distribution (Molecular Complexity)
        3. Molecular Structure Visualization (First 6 Drugs)
        """
        try:
            if not os.path.exists(self.data_path):
                self.logger.error(f"Dataset not found: {self.data_path}")
                return None

            df = pd.read_csv(self.data_path)
            os.makedirs(self.figure_dir, exist_ok=True)

            # 1️⃣ Label Distribution (0 = Non-permeable, 1 = Permeable)
            plt.figure(figsize=(6, 4))
            sns.countplot(x=df["Y"], palette="coolwarm")
            plt.xlabel("BBB Permeability (0 = No, 1 = Yes)")
            plt.ylabel("Count")
            plt.title("Label Distribution - Blood Brain Barrier Permeability")
            plt.savefig(os.path.join(self.figure_dir, "label_distribution.png"))
            plt.close()
            self.logger.info("✅ Label distribution saved.")

            # 2️⃣ SMILES Length Distribution (Molecular Complexity)
            df["SMILES_Length"] = df["Drug"].apply(len)
            plt.figure(figsize=(8, 5))
            sns.histplot(df["SMILES_Length"], bins=30, kde=True, color="purple")
            plt.xlabel("SMILES String Length")
            plt.ylabel("Frequency")
            plt.title("Distribution of Molecular Complexity (SMILES Length)")
            plt.savefig(os.path.join(self.figure_dir, "smiles_length_distribution.png"))
            plt.close()
            self.logger.info("✅ SMILES length distribution saved.")

            # 3️⃣ Visualizing Molecular Structures (First 6)
            smiles_list = df["Drug"].iloc[:6].tolist()
            mols = [Chem.MolFromSmiles(smiles) for smiles in smiles_list]
            img = Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(200, 200))

            img_path = os.path.join(self.figure_dir, "molecule_visualization.png")
            img.save(img_path)
            self.logger.info("✅ Molecular visualization saved.")

            self.logger.info("EDA visualizations completed and saved in 'figures' folder.")

        except Exception as e:
            self.logger.error(f"Error during EDA: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    eda = ExploratoryDataAnalysis()
    eda.generate_visuals()

