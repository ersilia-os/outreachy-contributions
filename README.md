# Outreachy contribution period

## Dataset: Tox21

### 🌟 Why Tox21?

For this modeling exercise, I have selected the **Tox21 dataset** from the Therapeutics Data Commons (TDC). The choice of Tox21 is motivated by its significance, structure, and applicability in the field of drug discovery and computational toxicology.

---

### 🔑 1. Relevance to Drug Discovery and Toxicity Screening
Tox21 addresses one of the key challenges in the drug discovery pipeline—**predicting chemical toxicity**. Toxicity is a primary cause of drug failure in clinical stages. Tox21 contains bioassay data that evaluates compounds' toxic effects across **12 well-defined biological targets**, including nuclear receptor signaling pathways (e.g., estrogen receptor, androgen receptor) and stress response pathways (e.g., p53, mitochondrial membrane potential).

By modeling toxicity at the early screening stage, Tox21 allows us to filter out potentially harmful compounds, contributing to safer and more efficient drug development.

---

### 📊 2. Binary Classification-Friendly Structure
Tox21 provides clear **binary classification labels (toxic/non-toxic)** for each compound, making it ideal for machine learning classification tasks. This aligns directly with our objective of building classification models, simplifying the data processing and model evaluation steps.

---

### 🚀 3. Well-Established Benchmark Dataset
Tox21 is recognized as a benchmark dataset in the computational chemistry and machine learning communities. It is widely used for evaluating the performance of ML and DL models in toxicity prediction, ensuring our results are reproducible and comparable.

According to the research paper **"A Comparative Study of Deep Learning Models and Classification Algorithms for Chemical Compound Identification and Tox21 Prediction" (2024)**, Tox21 has been used effectively to benchmark several deep learning models (ResNet50V2, InceptionV3, MobileNetV2, VGG19) and traditional ML models (Random Forest, KNN), demonstrating its robustness and versatility.

---

### 💻 4. Computational Feasibility
With ~8,000 compounds and 12 tasks, Tox21 is **large enough to support deep learning applications**, but small enough to be computationally manageable on standard hardware. Unlike large-scale datasets like BindingDB (millions of entries), Tox21 allows for faster iterations and experimentation.

---

### 🧍‍♂️ 5. Multi-Task Learning Potential
Each compound in Tox21 is annotated with **12 different toxicity labels**, enabling us to explore **multi-task learning models** that predict multiple toxicity endpoints simultaneously. This improves generalization and can offer deeper insights into compound behavior across biological systems.

---

### 🌍 6. Real-World Use Cases
The Tox21 dataset has several practical applications:

- **Drug Discovery:** Early identification of toxic compounds before costly clinical trials.
- **Chemical Safety:** Screening environmental chemicals for toxicity.
- **Off-Target Prediction:** Ensuring that compounds binding to target proteins do not adversely affect other pathways.
- **Regulatory Compliance:** Supporting chemical safety regulations by predicting potential harmful effects.

---

### 📚 7. Backed by Literature

Our selection is further supported by:

1. Huang, K., Fu, T., Gao, W., Zhao, Y., Roohani, Y., Leskovec, J., & Coley, C. W. (2021). *Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development*. NeurIPS 2021.

2. Alaca, Y., Emin, B., & Akgul, A. (2024). *A Comparative Study of Deep Learning Models and Classification Algorithms for Chemical Compound Identification and Tox21 Prediction*. Computers and Chemical Engineering, 189.

---

## Tox21 Data Processing and EDA

### Overview
This project consists of two Python scripts for handling the Tox21 dataset:
1. **Data Loading (`dataloader.py`)**: Defines a PyTorch Dataset class and functions to create DataLoaders for training, validation, and testing.
2. **Exploratory Data Analysis (`eda.py`)**: Performs exploratory data analysis (EDA) on the dataset, generating visualizations and summary reports.

### Installation
Ensure you have Conda installed. Create and activate a new Conda environment:
```bash
conda create --name tox21_env python=3.8
conda activate tox21_env
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Data Loading (`dataloader.py`)
#### Functionality
- Reads a Parquet file containing the Tox21 dataset.
- Splits the dataset into training, validation, and test sets.
- Converts data into a PyTorch-compatible Dataset and DataLoader.

### Usage Example
```python
from dataloader import get_dataloader

train_loader, valid_loader, test_loader = get_dataloader("../data/Single/tox21_NR-AR.parquet")
```
#### Arguments
- `data_path` (str): Path to the dataset.
- `batch_size` (int, default=32): Number of samples per batch.
- `shuffle` (bool, default=True): Whether to shuffle training data.
- `train_frac` (float, default=0.7): Training dataset fraction.
- `val_frac` (float, default=0.1): Validation dataset fraction.
- `test_frac` (float, default=0.2): Test dataset fraction.
- `seed` (int, default=42): Random seed for reproducibility.

### Exploratory Data Analysis (`eda.py`)
#### Functionality
- Performs basic statistics and visualization of the dataset.
- Generates an EDA report including:
  - Summary statistics
  - Missing values heatmap
  - Histograms of features
  - Boxplots for outlier detection

#### Usage
Run the script from the command line:
```bash
python eda.py --file path/to/dataset.parquet --output output_directory/
```
#### Arguments
- `--file` (str, required): Path to the dataset file (CSV or Parquet).
- `--output` (str, required): Directory to save EDA results.

#### Output Files
- `eda_report.txt`: Summary of dataset properties.
- `summary_statistics.csv`: Descriptive statistics.
- `missing_values_heatmap.png`: Visualization of missing data.
- `feature_distributions.png`: Histogram of feature distributions.
- `boxplot_outliers.png`: Boxplot for outlier detection.

#### Notebooks  
  - `tox21_data_exploration_all.ipynb` – This notebook performs a **exploratory data analysis (EDA)** across all 12 toxicity endpoints in the Tox21 dataset. 

  - `tox21_data_exploration_single.ipynb` – Instead of analyzing all endpoints together, this notebook focuses on **a single toxicity endpoint** at a time. It allows for a more detailed feature-wise exploration, including outlier detection and feature importance for a specific target.


### 📌 Key Inferences from EDA  

- **Missing Values:** The dataset has minimal missing values, making it ready for modeling with little preprocessing.  

- **Class Imbalance:** Some toxicity endpoints show class imbalance, requiring techniques like resampling or weighted loss functions.    
