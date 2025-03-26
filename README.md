# HTS HIV Prediction using Therapeutics Data Commons

## Project Overview
This project focuses on High-throughput screening (HTS) which is a critical component of small-molecule drug discovery in both industrial and academic research. We adopt using Machine learning models to predict experimental outcomes and save  time and costs. It basically helps to analyze a large variety of possible chemical compounds and use the ML predictions to filter out only the candidates that might have a high chance of being successful for further experiments which aids  researchers focus on the most promising candidates rather than random testings

In this we leverage ML to aid HTS by predicting HIV activity of small-molecule drugs using data from  [Therapeutics Data Commons (TDC)](https://tdcommons.ai/single_pred_tasks/hts). The goal is to develop a machine learning model that can process molecular structures and classify whether a given compound inhibits HIV replication.

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

### Installtion 
<!-- pip install git+https://github.com/ersilia-os/compound-embedding-lite.git -->
