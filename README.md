# Drug Response Prediction
This project focuses on predicting drug response using machine learning techniques. The dataset is downloaded from the [GDSC1 dataset](https://tdcommons.ai/multi_pred_tasks/drugres), which contains information about drug responses in various cell lines (177,310 pairs, 958 cancer cells and 208 drugs).

## Project Structure
```
├── scripts
│   ├── data_loader.py      # Script for downloading and loading the dataset
│   ├── preprocessor.py     # Script for preprocessing and comparing datasets
│
├── notebooks
│   ├── Drug Response Prediction.ipynb  # Jupyter notebook for analysis and modeling
│
├── models                  # Directory for storing trained models
│
├── data                    # Directory for storing datasets
│   ├── gdsc1.pkl      # The benchmarked dataset
│   ├── gdsc_gene_symbols.tab     # A tab-separated file containing the gene names for expressions of cell lines
│
├── README.md               # Project documentation
├── LICENSE                 # License information
```

# Download a Dataset of Interest
The dataset focuses on making accurations predictions on new set of drugs and cell-lines. It contains wet lab IC50 for different drugs (in form of SMILES) and 1000 cancer cell lines (in form of a RMD normalized gene expression)
The goal is to predict Y, the log normalized IC50

## Setup Instructions
### Prerequisites
- Python 3.12.9
- Jupyter Lab
- Required libraries: `tdc`, `pandas`, `shutil`

### Installation and Running the Project
1. Clone the forked repository into the project folder:
   ```bash
     git clone https://github.com/GentRoyal/outreachy-contribution
	 cd outreachy-contribution
   ```
2. Launch Jupyter
   ```bash
      jupyter lab
   ```
3. Navigate to `notebook/notebooks/Drug Response Prediction.ipynb` in the Notebook Environment
4. Run the notebook
5. The `notebooks/Drug Response Prediction.ipynb` notebook contains:
- Exploratory Data Analysis (EDA)
- Featuriser
- Machine Learning Model Training
- Performance Evaluation


## Understanding the Project Workflow
1. Download and Move the Dataset to `data\`
- The dataset is automatically fetched using the `DataDownloader` class in `scripts/data_loader.py`.
- Initially, the dataset will be downloaded in `notebook/` directory. This is Because our notebook is located in `notebook/` directory. 
- There is a need to move the downloaded data to the `data/` folder as required, and this is also automatically done with the `DataDownloader` 

Usage:
```python
from scripts.data_loader import DataDownloader
data_downloader = DataDownloader()
data, gdsc_df, gdsc_gene = data_downloader.fetch_gdsc1_dataset()
```

2. Preprocess the Benchmark Data
Here, the preprocessing script renames columns of the benchmark dataset and compares it with our original dataset to check if the benchmark dataframe is the same as the project dataset

Usage:
```python
from scripts.preprocessor import Preprocessor
preprocessor = Preprocessor(gdsc_df, benchmark_df)
comparison_result = preprocessor.compare_dataframes()
print(comparison_result)
```
