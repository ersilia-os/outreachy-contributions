# Toxicity Prediction Tasks (hERG Blockers)
This repository contain all the codes, dataset, scripts and figures used for the prediction of hERG blockers. The human either-a-go-go-related gene is a gene code for a potassium ion channel which is important for regulating heartbeat. We human take medications everytime for one or many purposes and we expect these medications to make us feel better. However, we can block our herg gene without knowing if we take drugs that is capable of blocking herg gene. Blocking this gene would cause a serious problem in the human system, so it is important that a model exist to help predict if a drug can block the herg gene and that is the essence of this project

## Overview
Specifically, I will be focus on creating a model that predicts whether a drug blocks the human ether-à-go-go related gene (hERG). The project is a **classification problem** and according to the project's dataset, each drug is represented by a drug id, a SMILES string and labeled as either blocking (1) or not blocking (0). The dataset includes 648 drugs and can be found under the [Toxicity Prediction Task](https://tdcommons.ai/single_pred_tasks/tox) in [TDCommons](https://tdcommons.ai/)

### Why this Project?
I must say that this wasn't the project I selected initially, I selected [DrugResponse - GDSC1](https://tdcommons.ai/multi_pred_tasks/drugres) but was informed it might get complicated especially when it gets to the featuriser stage and was advised to make a switch. So, I decided to carefully go through [TDCommons](https://tdcommons.ai/) again and I found hERG Blockers project under [Toxicity Prediction Task](https://tdcommons.ai/single_pred_tasks/tox). I am working on CareWomb, an AI/ML app that monitors maternal and fetal health, including heartbeats, to support safer pregnancies in remote areas. While the hERG blocker project and my CareWomb project are not directly related, I think there might be possiblities of conencting the two. The hERG blocker project is predicting whether drugs can block the hERG, and since the [hERG contributes to the electric activity of the heart](https://en.wikipedia.org/wiki/HERG#:~:text=This%20ion%20channel%20(sometimes%20simply%20denoted%20as%20%27hERG%27)%20is%20best%20known%20for%20its%20contribution%20to%20the%20electrical%20activity%20of%20the%20heart) and CareWomb tracks heatbeats, I think I can explore this possibility of linking the two projects and see where it leads.

### Task 1: Downloading the Dataset
#### Characteristics
- Drug_ID: Includes drug identifiers
- Drug: Represented by SMILES (Simplified Molecular Input Line Entry System) notation
- Y: Contains binary toxicity labels/classification (0 or 1)

There were 22 missing values in the `Drug_ID` column and I filled the missing values by combining the pubchempy and rdkit libraries. I started by extracting the molecule formula from the SMILES. This was then used to find the chemical formula and by extension, the drug name.
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

All through the project, I use a logger to log the process and the following is an extract
```bash
2025-03-26 09:32:58,292 - INFO - Processing 19 rows with missing Drug_IDs in ../data/hERG/train.csv...
2025-03-26 09:33:33,810 - INFO - Processed: {'SMILES': 'NC(=O)C[C@@H](N)c1nn[nH]n1', 'Formula': 'C4H8N6O', 'Name': 'MELAMINE FORMALDEHYDE', 'Drug_ID': 'MELAMINE FORMALDEHYDE'}
...
```
#### Repository Ogranization
```bash
.
├── data/               # Raw and processed dataset files
│   └── figures/        # Figures from EDA
│   └── hERG/           # hERG-specific data
│       ├── hERG.csv
│       ├── herg.tab
│       ├── test.csv
│       ├── train.csv
│       ├── validation.csv
│       ├── test_eos24ci_Featurised.csv
│       ├── train_eos24ci_Featurised.csv
│       └── validation_eos24ci_Featurised.csv
├── models/             # Saved machine learning model checkpoints
├── notebooks/          # Jupyter notebooks for analysis
│   └── TDC - Toxicity Prediction Task.ipynb
├── scripts/            # Python utility scripts
│   ├── main.py
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── explore.py
│   └── Featurise.py
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

#### Prerequisites
- Python 3.12.9 or later
- Conda
- Jupyter Lab (optional)
- WSL (optional)
- Docker (optional)

#### Loading Instructions
##### 1. Create Conda Environment
```bash
# Create a new conda environment
conda create --name ersilia python=3.12 -y
conda activate ersilia
```

##### 2. Install Dependencies
```bash
# Install required libraries
pip install -r requirements.txt
```

##### 3. Clone the Repository
```bash
git clone https://github.com/GentRoyal/outreachy-contribution.git
cd outreachy-contribution
```

##### How to Run
###### Method 1: Automation Script
```bash
cd scripts
python main.py
```
- You'll be prompted to enter a model name. Enter `hERG`
- You'll also be prompted whether you want to the existing dataset or download a new one. `Y` means that the existing preprocessed and Featurised data will be used and `N` means you're replacing the existing data with a new one and as such the prepeocessing, EDA and Featuriser steps will be performed.
- Note: For WSL users experiencing Matplotlib crashes, set Qt platform:
```bash
echo 'export QT_QPA_PLATFORM=offscreen' >> ~/.bashrc
source ~/.bashrc
```
Expected actions and results are as follows:
- This will automatically run `data_loader.py`, `data_processor`, `explore.py` and `Featurise.py` scripts
- Load and download the dataset
- Split the dataset into train, test and split
- Perform Exploratory Data Analysis (display dataset summary and generate visualization stored in `data\figures\hERG`)
- Featurise the dataset.

###### Method 2: Jupyter Notebook
1. Launch Jupyter Lab
   ```bash
   jupyter lab
   ```
2. Navigate to `notebook/notebooks/TDC - Toxicity Prediction Task.ipynb`
3. Run the notebook
4. Enter a valid model name
5. Expected results are same as method 1 with only difference being that visualizations are also displayed in the notebook

###### Sample Loading Result
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
- It is worth noting that the dataset was splitted using scaffold method of split. This is because I think we stand a chance of making sure that similar molecules don’t mix between our training, validation and test sets if we use scaffold split. By that we are truly testing our moddel on new data instead of a random split.
- Although this project runs the hERG dataset, it is capable of doing the same operations on the following datasets {'LD50_Zhu', 'ClinTox', 'Carcinogens_Lagunin', 'Skin Reaction', 'AMES', 'hERG', 'hERG_Karim', 'DILI'}

### Task 2: Featurisation
The choice of Featuriser for this project are based on two criterions
1. The Featuriser should be related to toxicity because it directly address the main goal of the project
2. The Featuriser be related to drugs as this would be related to the dataset.

The [Cardiotoxicity Classifier](https://github.com/ersilia-os/eos1pu1) featuriser which was my first go to featuriser, is directly related to toxicity which is very important for predicting hERG Blocker. It used SMILES representations of compounds which is present in our dataset and it captures the structure of a drug and its biological impact.
**Features**
- Uses biological data including gene expression and cellular paintings after drug interactions
- Classification is based on the chemical data such as SMILES representations of compounds
After Featurising the dataset, I got a Featurised dataset with `key` , `input` , `Probability` and `Prediction` as the columns. This does not really give me numerical features for me to work with.

Then I checked [DrugTax: Drug taxonomy](https://github.com/ersilia-os/eos24ci) which takes SMILES inputs and classifies the molecules according to their taxonomy (organic or inorganic), but this doesn't really have a direct relation with hERG blocking This Featuriser is easy to uses and it also uses a binary classification. 
In the end I got a vector of 163 features including the taxonomy classification.
Lastly, I checked the [ErG 2D Descriptors](https://github.com/ersilia-os/eos24ci) featuriser.
Because hERG blocking depends on molecular shape, functional groups, and pharmacophore properties, I will explore this featuriser too because it focuses on bioactivity, and it also captures pharmacophoric properties

```bash
2025-03-27 08:38:55,245 - INFO - Loading Ersilia model: eos5guo
Performing Featurisation...
2025-03-27 08:39:00,647 - INFO - Featurization completed in 5.40s for ../data/hERG/train.csv
2025-03-27 08:39:00,649 - INFO - Loading Ersilia model: eos5guo
2025-03-27 08:39:15,387 - INFO - Featurization completed in 14.74s for ../data/hERG/test.csv
2025-03-27 08:39:15,388 - INFO - Loading Ersilia model: eos5guo
2025-03-27 08:39:33,235 - INFO - Featurization completed in 17.85s for ../data/hERG/validation.csv
```

Today, 27/03/2025, I gave [Cardiotoxicity Classifier](https://github.com/ersilia-os/eos1pu1) a second look and I noticed it's not a featuriser but an actual classification model that predicts hERG Blockers. 
I'll use the result as a benchmark to evaluate my model performance.

### Task 3: Build an ML Model
