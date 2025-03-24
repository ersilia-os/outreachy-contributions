# TDC - hERG blockers Prediction
This project focuses on predicting whether an epitope binds to the TCR or not, given a epitope and a T-cell receptor using machine learning techniques. 

## Download a Dataset of Interest
The dataset is downloaded from the [herG blockers](https://tdcommons.ai/single_pred_tasks/tox/), 
and it contains information about drugs. This information is represented by a SMILES string and a drug ID. It also contain a label `Y` which is either blocking (1) or not blocking (0). 
The dataset includes 648 drugs, aiding in the assessment of cardiotoxicity risks and 
the goal of the project is to make a binary classification as to whether a drug blocks the human ether-à-go-go related gene (hERG).

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

2b. Method 2: Running The Notebook
1. Launch Jupyter
   ```bash
   jupyter lab
   ```
2. Navigate to `notebook/notebooks/TDC - hERG blockers.ipynb` and run the notebook

3.  Fix for WSL Users (If Matplotlib Crashes)  
If you encounter the Qt platform plugin "xcb" error, run the following commands:  
```bash
echo 'export QT_QPA_PLATFORM=offscreen' >> ~/.bashrc
source ~/.bashrc
```
This ensures that matplotlib runs in headless mode.

## Featuriser
Todo next...
