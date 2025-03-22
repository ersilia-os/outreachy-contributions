# Apply Ersilia Models to a modelling task

This involves three steps:
- Download a dataset
- Featurise the data
- Build an ML model

Setting the environment:

### Prerequisites
- linux OS
- gcc compiler, `sudo apt install build-essential`
- python 3.8 and above, [install here](https://www.python.org/).
- conda installed, use [Miniconda](https://docs.conda.io/en/latest/miniconda.html) Installer
- git installed, [install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- github cli installed, [Github CLI](https://cli.github.com/)
- gitlfs installed and activated, [Git LFS](https://git-lfs.github.com/)
- docker installed, [Docker](https://docs.docker.com/engine/install/)

### Installing Ersilia

All the prerequisites must be satisfied. 

- create a conda environment
  
`conda create -n ersilia python=3.12`

- activate the environment
  
`conda activate ersilia`

- clone ersilia repo
```
git clone https://github.com/ersilia-os/ersilia.git
cd ersilia
```

- install with pip 
`pip install -e .`

- confirm erisilia

`ersilia --help`

## Download a dataset

### Background of Data

This dataset falls under the Epitope domain within the Single prediction Problem category. It involves identifying the region on an antigen where an antibody can bind to trigger immune response. 

- Task Description: Prediction of amino acid token in the antigen's amino acid sequence, that is active in binding. This is a token-level classification

- Dataset size: 447 antigens

**Data source and curation**

The dataset was originally sourced from Protein Data Bank (PDB), a storage archive for structural data of proteins and other biological molecules. Scientists and researchers deposit newly discovered protein structure to PDB, where the data undergoes different stages, including collection, processing and validation. PDB ensures data consistency across deposition centers, maintaining data uniformity. Once reviewed, data is made available to the scientific community and the public.

To curate this dataset, BepiPred, a web tool was used. It predicts B-cell epitope and non-epitope amino acids from biomolecules, using a random forest algorithm trained on real antibody-antigen structures. Curated Dataset is stored in The Data Commons (TDC).

__Features__
- X (Input): Amino acid sequence of an antigen 
- Y (Output): A list of indices showing which amino acids in X are epitope

__Endpoint__

To produce a sequence-level prediction of epitope regions, helping researchers identify which parts of an antigen can trigger an immune response, which is of primary importance in vaccine and antibody development.

### Stey by step to downloading dataset from TDC

1- To retreive dataset from TDC, its python package has to be installed

`pip install pytdc` normal installation

`pip install "pytdc" "aiobotocore>=2.5,<3" "boto3>=1.37,<2" "botocore>=1.37,<2" "s3transfer>=0.5,<1"` to avoid any dependencies conflict

2- Using Notebook for an interactive session, can be found in notebooks/

- install jupyter notebook via conda `conda install -c conda-forge notebook` or
- install jupyter notebook via pip `pip install notebook`
- launch notebook from your root/ `jupyter notebook`
- retrieve the dataset from TDC
```
from tdc.single_pred import Epitope
data = Epitope(name = 'PDB_Jespersen')
```
- laod the dataset, converts it to pandas Dataframe for handling structure data in python

  `df = data.get_data()`

- save dataset in multiple format in data/ to keep it organized, .pkl saves by default in the working directory
```
df.to_csv("../data/raw_pdb_jesperson.csv", index=False)
df.to_pickle("../data/pdb_jesperson.pkl")
```

- explore features and basic info about dataset

`df.head()  # to show the first 5 rows`

`df.dtypes # to check data types`

`df.columns`

`df['Y'].dtype  # to check data type of target column`

```
split = data.get_split()
split.keys()  # splits are available
```

- name and save notebook `data_handling.ipynb` in the notebooks/

3- Using python scripts for automation and easily reproducible, this can be found in scripts/ 

- to download, load and save dataset, the script can easily be run 

`python data_handling.py`


Finally, dataset has been successfully downloaded, loaded and saved into the data/, notebook saved in the notebooks/ and script saved in scripts/

  








