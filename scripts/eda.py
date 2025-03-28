import argparse
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scripts.dataloader import DataLoader  # Import your DataLoader module

def perform_eda(df, output_dir):
    """Performs exploratory data analysis (EDA) on the dataset and saves results."""
    
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    log_file = os.path.join(output_dir, "eda_report.txt")
    stats_file = os.path.join(output_dir, "summary_statistics.csv")

    with open(log_file, "w") as f:
        f.write("### Basic Information:\n")
        f.write(str(df.info()) + "\n\n")

        f.write("### First 5 Rows:\n")
        f.write(df.head().to_string() + "\n\n")

        f.write(f"### Duplicate Rows: {df.duplicated().sum()}\n\n")

        f.write("### Missing Values:\n")
        missing_values = df.isnull().sum()
        f.write(missing_values[missing_values > 0].to_string() + "\n\n")

    # Save summary statistics
    df.describe().to_csv(stats_file)
    
    # Visualize missing values
    plt.figure(figsize=(10, 5))
    sns.heatmap(df.isnull(), cmap='viridis', cbar=False, yticklabels=False)
    plt.title("Missing Values Heatmap")
    plt.savefig(os.path.join(output_dir, "missing_values_heatmap.png"))
    plt.close()

    # Histogram of features
    df.hist(figsize=(12, 8), bins=30, edgecolor='black')
    plt.suptitle("Feature Distributions")
    plt.savefig(os.path.join(output_dir, "feature_distributions.png"))
    plt.close()

    # Boxplots for outlier detection
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df.select_dtypes(include=['float64', 'int64']), palette="Set2")
    plt.xticks(rotation=45)
    plt.title("Boxplot for Outlier Detection")
    plt.savefig(os.path.join(output_dir, "boxplot_outliers.png"))
    plt.close()

    print("\nEDA Completed Successfully! Results saved in:", output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform EDA on a given dataset and save results.")
    parser.add_argument("--file", type=str, required=True, help="Path to the dataset file (CSV/Parquet)")
    parser.add_argument("--output", type=str, required=True, help="Directory to save EDA results")
    args = parser.parse_args()

    # Use DataLoader to load data
    data_loader = DataLoader(args.file)
    df = data_loader.load_data()

    perform_eda(df, args.output)
