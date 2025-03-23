import os
import pandas as pd
import seaborn as sns
import logging

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

class ExploratoryDataAnalysis:
    def __init__(self, data_path="../data/weber.csv", figure_dir="../figures/"):
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
        Generates and saves EDA visualizations.
        """
        try:
            if not os.path.exists(self.data_path):
                self.logger.error(f"Processed data file not found: {self.data_path}")
                return None

            df = pd.read_csv(self.data_path)

            # Ensure figure directory exists
            os.makedirs(self.figure_dir, exist_ok=True)

            # 1. Label Distribution
            plt.figure(figsize=(10, 5))
            sns.barplot(x=df.label.value_counts().index, y=df.label.value_counts().values)
            plt.xlabel("Labels")
            plt.ylabel("Count")
            plt.title("Label Distribution")
            plt.savefig(os.path.join(self.figure_dir, "label_distribution.png"))
            plt.close()

            # 2. Epitope Length Distribution
            epitope_length = df['epitope_aa'].str.len()
            sns.histplot(epitope_length, bins=20, kde=True)
            plt.title("Epitope Sequence Length Distribution")
            plt.savefig(os.path.join(self.figure_dir, "epitope_length.png"))
            plt.close()

            # 3. TCR Length Distribution
            tcr_length = df['tcr'].str.len()
            sns.histplot(tcr_length, bins=20, kde=True)
            plt.title("TCR Sequence Length Distribution")
            plt.savefig(os.path.join(self.figure_dir, "tcr_length.png"))
            plt.close()

            # 4. Epitope vs Label Heatmap
            pivot_table = df.pivot_table(index='epitope_aa', columns='label', aggfunc='size', fill_value=0).head(20)
            sns.heatmap(pivot_table, cmap="Blues", annot=True, fmt="d")
            plt.title("Epitope vs. Label Heatmap")
            plt.savefig(os.path.join(self.figure_dir, "epitope_vs_label_heatmap.png"))
            plt.close()

            self.logger.info("EDA visualizations saved in figures/ folder.")
        except Exception as e:
            self.logger.error(f"Error during EDA: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    eda = ExploratoryDataAnalysis()
    eda.generate_visuals()
