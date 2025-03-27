# HTS HIV Prediction using Therapeutics Data Commons

## Project Overview
This project focuses on High-throughput screening (HTS) which is a critical component of small-molecule drug discovery in both industrial and academic research. We adopt using Machine learning models to predict experimental outcomes and save  time and costs. It basically helps to analyze a large variety of possible chemical compounds and use the ML predictions to filter out only the candidates that might have a high chance of being successful for further experiments which aids  researchers focus on the most promising candidates rather than random testings

In this we leverage ML to aid HTS by predicting HIV activity of small-molecule drugs using data from  [Therapeutics Data Commons (TDC)](https://tdcommons.ai/single_pred_tasks/hts). The goal is to develop a machine learning model that can process molecular structures and classify whether a given compound inhibits HIV replication.

#### Reason for choice of dataset:
- HIV is a chronic global health problem for which there is no cure, and new drug candidates are urgently required to target drug-resistant strains of HIV
- traditional HTS of HIV inhibitors is time-consuming and costly, but ML models can accelerate screening by predicting molecular activity, reducing laboratory testing

### HTS HIV Prediction Task & Dataset Overview
**Task Description:** Binary classification task(active vs. inactive compounds) given a drug SMILES string as input to predict its activity against HIV virus.

**Dataset Description:** The HIV dataset was introduced by the Drug Therapeutics Program (DTP) AIDS Antiviral Screen, which tested the ability to inhibit HIV replication for over 40,000 compounds. From [MoleculeNet](https://moleculenet.org/datasets-1).


**Dataset Statistics:** 41,127 drugs.

### Repository Structure
```bash
.
├── Makefile        # Automate run processes
├── README.md       # Project documentation  
├── data            # includes raw and processed dataset files  
│   ├── featurized
│   └── raw
├── models          # Saved models and training artifacts  
├── notebooks       # Jupyter notebooks for analysis 
└── scripts         # Python scripts for data processing
```

### Setup & Installation 

#### Prerequisites
The Prerequisites for this setup includes:
- conda (Python 3.9+) 
- python 3.9+

#### usage
- create a virtual environment and activate it with conda or any python virtual environment module 

- clone the repository
    ```bash
    git clone git@github.com:Bee0933/outreachy-contributions.git
    ```
 > *Note: for ease of use and replication I included a Makefile to run the processes*
- Install packages 
    ```bash
    make install-packages
    ```
    This basically installs `pytdc` package to download and manipulate data from the [TDC data repository](https://tdcommons.ai/) and a python wrapper I found for the [Ersilia compound embeddings model](https://github.com/ersilia-os/compound-embedding-lite) which enables one to programically integrate the model to any python code to produce embeddings of 1024 features from small molecules.
    *(This prepares the environment to run the futher processes for the project)*

#### Downloading the Dataset
The dataset download process involves using a python script to pull the required data from the TDC dataset reopository which includes curated AI-ready datasets for single-instance, multi-instance pedictions and generation. [The dataset download script](scripts/load_data.py) allows one to specify any of the datasets from the single instance [High-throughput Screening Prediction Task](https://tdcommons.ai/single_pred_tasks/hts) such as `HIV` or `SARSCoV2_3CLPro_Diamond` and the preferred local storage path for the data in the [env](scripts/.env) file which contains all the dynamic variables to run the scripts 

```bash
#filename: .env
LOCAL_DATA_PATH="../data"
HTS_DATASET_NAME="HIV"
```
The script retrieves TDC HTS single instance prediction data based on the specified dataset and splits the data using `scaffold` method by default to the ratio of [0.7, 0.1, 0.2] for train/val/test and stores it in data folder under a `raw` sub folder. `scaffold` split was a preffered choice because it ensures better generalization example, preventing data leakage where if similar data exist in both training and testing sets, the model might memorize features rather than learning general patterns, leading to overestimated predictive power.

The computational feasibility of the dataset is included [here](notebooks/computational-assessment.ipynb)

run the script with:
```bash
make load-tdc-data
```
or manually modify and run in the [script](scripts/load_data.py)
run the script with:
```bash
python load_data.py
```

#### Featurizing the Data
The featurization process involves using the [featurize_data](scripts/featurize_data.py) script to create descriptors from the loaded data done with the [load_data script](scripts/load_data.py). I used Ersilia Compound Embeddings to create embeddings for the small-molecule data because;
- unlike other traditional fingerprints, ts includes both physicochemical properties and bioactivity data, making it more informative for HTS task
- the embeddings leverage a pretrained network trained on FS-Mol and ChEMBL datasets, allowing them to generalize well across structurally diverse compounds, which inm my opinion is quite essential for drug discovery  and,
- each molecule is encoded into a 1024-dimensional feature vector, preserving key molecular characteristics while enabling efficient similarity comparisons.
This was refferenced from the model description on [Ersilia Model Hub](https://www.ersilia.io/model-hub)

The script featurizes the donloaded CSV files in the `data/raw` folder using the Ersilia Compound Embeddings model [python wrapper](https://github.com/ersilia-os/compound-embedding-lite) to produce embeddings of 1024 features for small molecules.
The script allows one to specify the `smiles_column` on the dataset that contains the small-molecules and is optimized to read the data data and creates embeddings in batches to prevent memory overload on computation since its using a model to make predictions on the dataset values. The processed data is saved as parquet for reasons of efficient storage and chema enforcement in the `data/featurized` folder

run the script with:
```bash
make featurize-data
```
or manually modify and run in the [script](scripts/featurize_data.py)
run the script with:
```bash
python featurize_data.py
```

#### Running the whole process
we can run the whole process with 
```bash
make all
```


#### References
- [TDS High-throughput Screening](https://tdcommons.ai/single_pred_tasks/hts)
- [Ersilia Model Hub](https://www.ersilia.io/model-hub)

<!-- pip install git+https://github.com/ersilia-os/compound-embedding-lite.git -->
