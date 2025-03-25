## Apply Ersilia Models to a modelling task

### Project steps:
1. [Download a dataset](https://github.com/AzeematRaji/ersilia-outreachy/edit/main/README.md#download-a-dataset)
1. [Featurise the data](https://github.com/AzeematRaji/ersilia-outreachy/edit/main/README.md#featurising-the-data)
1. Build an ML model

Setting the environment:

#### Prerequisites
- linux OS
- gcc compiler, `sudo apt install build-essential`
- python 3.8 and above, [install here](https://www.python.org/).
- conda installed, use [Miniconda](https://docs.conda.io/en/latest/miniconda.html) Installer
- git installed, [install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- github cli installed, [Github CLI](https://cli.github.com/)
- gitlfs installed and activated, [Git LFS](https://git-lfs.github.com/)
- docker installed, [Docker](https://docs.docker.com/engine/install/)

#### Installing Ersilia

All the prerequisites must be satisfied. 

create a conda environment:
  
`conda create -n ersilia python=3.12`

activate the environment:
  
`conda activate ersilia`

clone ersilia repo:
```
git clone https://github.com/ersilia-os/ersilia.git
cd ersilia
```

install with pip:

`pip install -e .`

confirm erisilia:

`ersilia --help`

### Download a dataset

#### Background of Data

__Dataset__: _Bioavailability, Ma et al._

Oral bioavailability is the fraction of an orally administered drug that reaches site of action in an unchanged form.
It is influenced by factors like absorption, metabolism and solubility

__Task__: Given a drug ("SMILES"), predict the activity of bioavailability in Binary (0 or 1)

- Bioavailable - 1 
- Not Bioavailable - 0

__Size__: 640 drug molecules

__Source__: TDC (Therapeutics Data Commons), a collection of curated datasets and tools to apply machine learning in drug discovery

#### Steps to downloading dataset from TDC

1- To retreive dataset from TDC, install its python package:

`pip install pytdc` normal installation

`pip install "pytdc" "aiobotocore>=2.5,<3" "boto3>=1.37,<2" "botocore>=1.37,<2" "s3transfer>=0.5,<1"` to avoid any dependencies conflict

2- Using Notebook for an interactive session, can be found in notebooks/

Set up notebook:
- install jupyter notebook via conda `conda install -c conda-forge notebook` or
- install jupyter notebook via pip `pip install notebook`
- launch notebook from your root/ `jupyter notebook`

retrieve the dataset from TDC:
```
from tdc.single_pred import ADME
data = ADME(name = 'Bioavailability_Ma')
```
load the dataset in pandas Dataframe for handling structured data in python:

  `df = data.get_data()`

save dataset in .csv format in data/ to keep it organized, .tab saves by default in the working directory
```
df.to_csv("../data/bioavailability.csv", index=False)
```

explore features and basic info about dataset

`df.head()  # to show the first 5 rows`

`df.dtypes # to check data types`

`df.columns`

`df['Y'].dtype  # to check data type of target column`

```
split = data.get_split()
split.keys()  # splits are available
```

save notebook `data_handling.ipynb` in the notebooks/

3- Using python scripts for automation and easily reproducible, this can be found in scripts/ 

to download, load and save dataset, the script can easily be run using:

`python ./scripts/data_handling.py`


Dataset has been successfully downloaded, loaded and saved into the data/, notebook saved in the notebooks/ and script saved in scripts/.

### Featurising the data

__Featuriser__: _Ersilia Compound Embeddings_ (eos2gw4)

This is useful in predicting bioavailability, because it encodes chemical and bioactivity information of drug molecules not just the structure. Therefore providing comprehensive molecular representation and since bioavailability is influenced by chemical structure, physicochemical properties and biology activity, its better suited. Also it is pretrained on bioactive molecules from FS-Mol and chEMBL, which ensures it captures meaningful patterns from well-established datasets and similarities between drugs which make machine learning generalize better.

#### Steps to featurise the data:

Since the featuriser is a representation model from ersilia hub, and previously installed [ersilia](https://github.com/AzeematRaji/ersilia-outreachy/edit/main/README.md#installing-ersilia)

1- fetch the model:

`ersilia fetch eos2gw4`

2- serve the model:

`ersilia serve eos2gw4`

3- run, passing the saved dataset as the input, specify the output in a file:

`ersilia run -i ./data/bioavailabilty.csv -o ./data/featurised_bioavailability.csv`

this will take your dataset and return a featurised dataset in the file specified.

4- Using python scripts for automation and easily reproducible, can be found /scripts. run:
`python ./scripts/bio_data_featurising.py`

this will return a featurised dataset in the data/ successfully.








