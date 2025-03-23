# TCR-Epitope Binding Affinity Prediction
This project focuses on predicting whether an epitope binds to the TCR or not, given a epitope and a T-cell receptor using machine learning techniques. 

## Download a Dataset of Interest
The dataset is downloaded from the [Weber dataset](https://tdcommons.ai/multi_pred_tasks/tcrepitope), and it contains amino acid sequences either for the entire TCR or only for the hypervariable CDR3 loop
Originally, the dataset was imbalance, but was downsampled to a limit of 400 TCRs per epitope
The goal is to make predictions as to whether an epitope binds to the TCR or not.

### Setup Instructions
#### Prerequisites
- Python 3.12.9
- Jupyter Lab
- Required libraries: `conda`, `tdc`, `pandas`, `shutil`

#### How to Run
1. Clone the forked repository into the project folder:
   ```bash
   git clone https://github.com/GentRoyal/outreachy-contribution
   conda activate ersilia
   cd outreachy-contribution
   ```

##### Method 1: Run the Automation Script
   ```bash
   python scripts/main.py
   ```

##### Method 2: Running The Notebook
1. Launch Jupyter
   ```bash
   jupyter lab
   ```
2. Navigate to `notebook/notebooks/TCR-Epitope Binding Affinity Prediction.ipynb` and run the notebook

##### Fix for WSL Users (If Matplotlib Crashes)  
If you encounter the Qt platform plugin "xcb" error, run the following commands:  
```bash
echo 'export QT_QPA_PLATFORM=offscreen' >> ~/.bashrc
source ~/.bashrc
```
This ensures that matplotlib runs in headless mode.

## Featuriser
Todo next...
