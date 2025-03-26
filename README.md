# Toxicity Prediction Tasks (hERG Blockers)

## Overview
The overall task focuses on predicting the toxicity of drug molecules towards human organisms. Specifically, I will be focusing on hERG blockers which is to predict whether a drug blocks the human ether-à-go-go related gene (hERG).
The project is a **classification problem**, where each drug is represented by its SMILES string and labeled as either blocking (1) or not blocking (0). The dataset includes 648 drugs, aiding in the assessment of cardiotoxicity risks.

### Why?
I am working on CareWomb, an AI/ML app that monitors maternal and fetal health, including heartbeats, to support safer pregnancies in remote areas. While the hERG blocker project and my CareWomb project are not directly related, I think there might be possiblities of conencting the two. The hERG blocker project is predicting whether drugs can block the hERG, and since the [hERG contributes to the electric activity of the heart](https://en.wikipedia.org/wiki/HERG#:~:text=This%20ion%20channel%20(sometimes%20simply%20denoted%20as%20%27hERG%27)%20is%20best%20known%20for%20its%20contribution%20to%20the%20electrical%20activity%20of%20the%20heart) and CareWomb tracks heatbeats, I think I can explore this possibility of linking the two projects and see where it leads.

### About the Data
#### Dataset Background and Endpoint
From the [abstract of the literature attached to the task description](https://pubs.acs.org/doi/10.1021/acs.molpharmaceut.6b00471), the project is experimenting on predicting hERG liability, which means determining whether compounds will block the hERG channel or not

#### Threshold
The blockage of hERG channel risk is measured by pIC50 values. The pIC50 measure is a way to find how strong a drug is at blocking a process in the body
The threshold estimated from the supporting document of the project dataset is pIC50 values ≤4.391 as 0 (i.e. no blockers) and pIC50 values >4.391 as 1 (non-blockers)

#### Dataset Composition
- Drug_ID: Includes drug identifiers
- Drug: Represented by SMILES (Simplified Molecular Input Line Entry System) notation
- Y: Contains binary toxicity labels/classification (0 or 1)

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 655 entries, 0 to 654
Data columns (total 3 columns):
 #   Column   Non-Null Count  Dtype  
---  ------   --------------  -----  
 0   Drug_ID  633 non-null    object 
 1   Drug     655 non-null    object 
 2   Y        655 non-null    float64
dtypes: float64(1), object(2)
memory usage: 15.5+ KB
```
The missing values in the `Drug_ID` Column were filled by combining the pubchempy and rdkit libraries.
I started by extracting the molecule formula from the SMILES. This was then used to find the chemical formula and by extension, the drug name.
```bash
	smile = row["Drug"]
	mol = Chem.MolFromSmiles(smile)
	if mol:
		formula = rdMolDescriptors.CalcMolFormula(mol)
		try:
			compounds = pcp.get_compounds(formula, 'formula')
			if compounds:
				name = compounds[0].synonyms[0] if compounds[0].synonyms else compounds[0].iupac_name
			else:
				name = formula  # Fallback to formula

```

The process was logged and the following is an extract from the log.
```bash
2025-03-26 09:32:58,292 - INFO - Processing 19 rows with missing Drug_IDs in ../data/hERG/train.csv...
2025-03-26 09:33:33,810 - INFO - Processed: {'SMILES': 'NC(=O)C[C@@H](N)c1nn[nH]n1', 'Formula': 'C4H8N6O', 'Name': 'MELAMINE FORMALDEHYDE', 'Drug_ID': 'MELAMINE FORMALDEHYDE'}
...
```

## Project Structure
```bash
.
├── data/               # Raw and processed dataset files
│   └── hERG/           # hERG-specific data
│       ├── hERG.csv
│       ├── herg.tab
│       ├── test.csv
│       ├── train.csv
│       ├── validation.csv
│       ├── test_eos24ci_featurized.csv
│       ├── train_eos24ci_featurized.csv
│       └── validation_eos24ci_featurized.csv
├── figures/            # Visualization outputs
│   └── hERG/           # hERG-specific visualizations
├── models/             # Saved machine learning model checkpoints
├── notebooks/          # Jupyter notebooks for analysis
│   └── TDC - Toxicity Prediction Task.ipynb
├── scripts/            # Python utility scripts
│   ├── main.py
│   ├── data_loader.py
│   ├── explore.py
│   └── featurize.py
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Prerequisites
- Python 3.12.9 or later
- Conda
- Jupyter Lab (optional)
- WSL (optional)
- Docker (optional)

## Loading Instructions
### 1. Create Conda Environment
```bash
# Create a new conda environment
conda create --name ersilia python=3.12 -y
conda activate ersilia
```

### 2. Install Dependencies
```bash
# Install required libraries
pip install -r requirements.txt
```

### 3. Clone the Repository
```bash
git clone https://github.com/GentRoyal/outreachy-contribution.git
cd outreachy-contribution
```

## How to Run
### Method 1: Automation Script
```bash
python scripts/main.py
```
- You'll be prompted to enter a model name
- Note: For WSL users experiencing Matplotlib crashes, set Qt platform:
  ```bash
  echo 'export QT_QPA_PLATFORM=offscreen' >> ~/.bashrc
  source ~/.bashrc
  ```
Expected actions and results are as follows:
- This will automatically run `data_loader.py`, `explore.py` and `featurize.py` scripts
- Load and download the dataset
- Split the dataset into train, test and split
- Perform Exploratory Data Analysis (display dataset summary and generate visualization stored in `data\figures\hERG`)
- Featurize the dataset. At this stage, you have the option to select an already featurized dataset or give a prompt to featurize the dataset again

### Method 2: Jupyter Notebook
1. Launch Jupyter Lab
   ```bash
   jupyter lab
   ```
2. Navigate to `notebook/notebooks/TDC - Toxicity Prediction Task.ipynb`
3. Run the notebook
4. Enter a valid model name
5. Expected results are same as method 1 with only difference being that visualizations are also displayed in the notebook

### Sample Loading Result
```bash
2025-03-24 22:52:00,772 - INFO - Downloading 'hERG' dataset...
Downloading...
100%|██████████████████| 50.2k/50.2k [00:00<00:00, 241kiB/s]
Loading...
Done!
2025-03-24 22:52:03,325 - INFO - Dataset 'hERG' saved to /home/gentroyal/outreachy-temp/data/hERG/hERG.csv (Shape: (655, 3))
2025-03-24 22:52:03,326 - INFO - Splitting dataset using 'scaffold' method...
100%|███████████████████| 655/655 [00:00<00:00, 1854.63it/s]
2025-03-24 22:52:03,695 - INFO - Train set saved (Shape: (458, 3))
2025-03-24 22:52:03,696 - INFO - Validation set saved (Shape: (65, 3))
2025-03-24 22:52:03,698 - INFO - Test set saved (Shape: (132, 3))
```
- It is worth noting that the dataset was splitted using scaffold method of split. This is because we stand a chance of making sure that similar molecules don’t mix between our training, validation and test sets if we use scaffold split. So our moddel is truly tested on new data than random split.
- Also, the functions use logging to track all operations (from loading the dataset, moving it to the correct location and splitting it to train, test and validation, data exploration, featurization, etc.). This helps us debug when our code breaks down.
- Although this project runs the hERG dataset, it is capable of doing the same operations on the following datasets {'LD50_Zhu', 'ClinTox', 'Carcinogens_Lagunin', 'Skin Reaction', 'AMES', 'hERG', 'hERG_Karim', 'DILI'}

## Featurization Steps
The choice of featurizer for this project are based on two criterions
1. The featurizer should be related to toxicity because it directly address the main goal of the project
2. The featurizer be related to drugs as this would be related to the dataset.

### [Cardiotoxicity Classifier](https://github.com/ersilia-os/eos1pu1)
This featuriser is directly related to toxicity which is very important for predicting hERG Blocker. It used SMILES representations of compounds which is present in our dataset and it captures the structure of a drug and its biological impact. 
**Features**
- Uses biological data including gene expression and cellular paintings after drug interactions
- Classification is based on the chemical data such as SMILES representations of compounds
- Also uses Morgan fingerprints and Mordred physicochemical descriptors to describe the molecular structure of the drug interactions
### Problem Encountered
After featurizing the dataset, I got a featurized dataset with `key` , `input` , `Probability` and `Prediction` as the columns. 
This does not enerate numerical features for me to work with.

### [DrugTax: Drug taxonomy](https://github.com/ersilia-os/eos24ci)
**Features**
- Takes SMILES inputs
- Classifies the molecules according to their taxonomy (organic or inorganic)
- Uses a binary classification for each
In the end I got a vector of 163 features including the taxonomy classification.

```bash
2025-03-26 09:40:12,134 - INFO - Loading Ersilia model: eos24ci
2025-03-26 09:41:59,316 - INFO - Featurization completed in 107.18s for ../data/hERG/train.csv
2025-03-26 09:41:59,319 - INFO - Loading Ersilia model: eos24ci
2025-03-26 09:42:32,077 - INFO - Featurization completed in 32.76s for ../data/hERG/test.csv
2025-03-26 09:42:32,079 - INFO - Loading Ersilia model: eos24ci
2025-03-26 09:43:02,010 - INFO - Featurization completed in 29.93s for ../data/hERG/validation.csv
```