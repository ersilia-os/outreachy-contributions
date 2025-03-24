import os
import pandas as pd
import seaborn as sns
import logging
from rdkit import Chem
from rdkit.Chem import Draw
import matplotlib
matplotlib.use('Agg')  # This is correct for non-interactive backends
import matplotlib.pyplot as plt

class ExploratoryDataAnalysis:
    def __init__(self, data_path="data/herg.csv", figure_dir="figures/"):
        self.data_path = data_path
        self.figure_dir = figure_dir
        
        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)
        
        # Print absolute paths for debugging
        self.logger.info(f"Absolute data path: {os.path.abspath(data_path)}")
        self.logger.info(f"Absolute figure directory: {os.path.abspath(figure_dir)}")
    
    def generate_visuals(self):
        """
        Generates and saves EDA visualizations.
        """
        try:
            if not os.path.exists(self.data_path):
                self.logger.error(f"Processed data file not found: {self.data_path}")
                return None
                
            df = pd.read_csv(self.data_path)
            
            # Ensure figure directory exists
            os.makedirs(self.figure_dir, exist_ok=True)
            self.logger.info(f"Figure directory created/verified at: {os.path.abspath(self.figure_dir)}")
            
            # 1. Label Distribution
            counts = dict(df.Y.value_counts()).items()
            for key, value in counts:
                classification = "blockers" if key == 1.0 else "non-blockers"
                print(f"{value} drugs are classified as {classification}")
            
            plt.figure(figsize=(10, 5))
            sns.barplot(x=df.Y.value_counts().index, y=df.Y.value_counts().values)
            plt.xlabel("Labels")
            plt.ylabel("Count")
            plt.title("Label Distribution")
            
            fig_path = os.path.join(self.figure_dir, "label_distribution.png")
            plt.savefig(fig_path)
            self.logger.info(f"Saved figure to: {os.path.abspath(fig_path)}")
            plt.close()
            
            # 2. SIMILE Length Distribution
            plt.figure(figsize=(10, 5))
            simile_length = df['Drug'].str.len()
            sns.histplot(simile_length, bins=20, kde=True)
            plt.title("SIMILE Length Distribution")
            
            fig_path = os.path.join(self.figure_dir, "simile_length.png")
            plt.savefig(fig_path)
            self.logger.info(f"Saved figure to: {os.path.abspath(fig_path)}")
            plt.close()
            
            # 3. Molecules to Grid of first three drugs
            smiles_list = df["Drug"].iloc[:3].tolist() 
            drug_names = df["Drug_ID"].iloc[:3].tolist()
            mols = [Chem.MolFromSmiles(smiles) for smiles in smiles_list]
            img = Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(300, 300), legends=drug_names)
            
            img_path = os.path.join(self.figure_dir, "molecule_grid.png")
            img.save(img_path)
            self.logger.info(f"Saved molecule grid to: {os.path.abspath(img_path)}")
            
            self.logger.info("EDA visualizations saved in figures folder.")
        except Exception as e:
            self.logger.error(f"Error during EDA: {e}", exc_info=True)
            return None

# Add code to actually run the analysis
if __name__ == "__main__":
    eda = ExploratoryDataAnalysis()
    eda.generate_visuals()
    print("EDA process completed.")