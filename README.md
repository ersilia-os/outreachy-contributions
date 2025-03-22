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

#### Installation and Running the Project
1. Clone the forked repository into the project folder:
   ```bash
   git clone https://github.com/GentRoyal/outreachy-contribution
   conda activate ersilia
   cd outreachy-contribution
   ```
2. Launch Jupyter
   ```bash
   jupyter lab
   ```
2. Navigate to `notebook/notebooks/TCR-Epitope Binding Affinity Prediction.ipynb` and run the notebook

#### Understanding the Project Workflow
1. Download and Move the Dataset to `data\`
- The dataset is automatically fetched using the `DataDownloader` class in `scripts/data_loader.py`.
- Initially, the dataset will be downloaded in `notebook/` directory. This is Because our notebook is located in `notebook/` directory. 
- There is a need to move the downloaded data to the `data/` folder as required, and this is also automatically done with the `DataDownloader` 

Usage:
```python
from scripts.data_loader import DataDownloader
downloader = DataDownloader()
data, df = downloader.fetch_weber_dataset()
```

2. Run the Notebook to view the results of the EDA

## Featuriser
Todo next...
