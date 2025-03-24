# TDC - Toxicity Prediction Tasks (hERG blockers and AMES)
- Project 1. The overall task focuses on predicting the toxicity of drug molecules towards human organisms. Specifically, I will be focusing on hERG blockers which is to predict whether a drug blocks the human ether-à-go-go related gene (hERG).
- Project 2. This project is also under toxicity prediction task and its overall goal is on predicting whether a drug SMILES string is mutagenic or not.

## Download a Dataset of Interest
- Both datasets are downloaded from the [Toxicity Prediction](https://tdcommons.ai/single_pred_tasks/tox/), and they contains information about drugs. 
- This information is represented by a SMILES string and a drug ID. They also contain a label `Y` 
- For hERG: The label Y is either blocking (1) or not blocking (0). 
- For AMES: The label Y is either mutagens (1) or non mutagens (0). 

### Setup Instructions
#### Prerequisites
- Python 3.12.9 or later
- Jupyter Lab
- Conda
- WSL 
- Docker
- Required libraries: `tdc`, `ersilia`, `pandas`, `numpy`, `seaborn`, `matplotlib`, `rdkit`

#### How to Run
1. Clone the forked repository into the project folder:
   ```bash
	conda create --name ersilia python=3.12 -y
	conda activate ersilia

	# Clone the repository and navigate into it
	git clone https://github.com/GentRoyal/outreachy-contribution
	cd outreachy-contribution

   ```

2a. Method 1: Run the Automation Script
   ```bash
   python scripts/main.py
   ```
   You'll get a prompt to enter a model name
   
   Fix for WSL Users (If Matplotlib Crashes)  
   If you encounter the Qt platform plugin "xcb" error, run the following commands:  
   ```bash
   echo 'export QT_QPA_PLATFORM=offscreen' >> ~/.bashrc
   source ~/.bashrc
   ```
   This ensures that matplotlib runs in headless mode.


2b. Method 2: Running The Notebook
1. Launch Jupyter
   ```bash
   jupyter lab
   ```
2. Navigate to `notebook/notebooks/TDC - Toxicity Prediction Task.ipynb`
3. Enter a valid model name 
4. Run the notebook

## Featuriser
Todo next...