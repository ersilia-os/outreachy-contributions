# Outreachy Contribution: DILI Prediction with Ersilia Model Hub

 This pull request focuses on the data selection, loading, inspection, and featurization steps for the DILIdataset, which predicts drug-induced liver injury (DILI). 

## Project Goals
- Understand how to use and interact with the Ersilia Model Hub.
- Demonstrate basic AI/ML knowledge through a drug discovery task.
- Test Python coding skills and thorough documentation.


## Data Selection: Why DILIdataset?
I chose the DILIdataset from the Therapeutics Data Commons (TDC) for the following reasons:
- **Relevance to my local community's Health Needs (Cameroon):** Drug-induced liver injury is a critical concern in Cameroon, where diseases like HIV, TB, and malaria are treated with drugs that can cause liver toxicity. For example, antimalarial drugs can lead to liver enzyme abnormalities, impacting patient safety ([Impact of Malaria on Liver Enzymes](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6592410/)).
Also, people in local communities and fund of "self medicating", which also poses a problem in taking drugs that are not prescribed.
- **Contribution to Ersilia's Mission:** This work aligns with Ersilia's goal of expanding AI/ML models for biomedical research, improving drug safety in underserved regions.
- **Classifier Suitability:** Considering binary classification, the dataset(with 475 drugs) is manageable and suitable for modeling within the given period.

## Data Loading and Inspection
The DILIdataset was obtained externally due to challenges installing PyTDC. The dataset consists of four CSV files, stored in the `data` folder:
- `dili_full.csv`: Full dataset with 475 drugs.
- `dili_train.csv`: Training set with 332 drugs.
- `dili_test.csv`: Test set with 95 drugs.
- `dili_valid.csv`: Validation set with 48 drugs.

Each file contains three columns:
- `Drug_ID`: The unique classifier for each drug (datatype = nfloat64).
- `Drug`: SMILES string representing molecular structure (datatype = object).
- `Y`: Binary label (datatype = float64, 0.0 for no liver injury, 1.0 for liver injury).

The data was loaded and inpected to understand its characteristics, structure and quality using pandas in the notebook `notebooks/01_data_download_inspection.ipynb` 

### Understanding the data:
*Structure*: The dataset has 475 drugs, split into training (332 drugs), test (95 drugs), and validation (48 drugs) sets. Each entry includes a drug ID, SMILES string, and binary label.
*Data Quality*: No missing values were found in any split.

*Data visualisation*:
I generated two plots to visualize the data, which are saved in the `data` folder:
- Class Distribution: A bar plot showing the count of positive and negative labels in the training set. 
- SMILES Length Distribution: A histogram with a kernel density estimate, showing a right-skewed distribution. Most SMILES strings are between 20 and 80 characters, with a few outliers exceeding 100 characters.
## Featurization
I featurized the SMILES strings using the `eos4wt0` model from the Ersilia Model Hub, which generates Morgan Fingerprints—a 2048-bit binary representation of molecular substructures. This step was performed in `notebooks/02_featurization.ipynb`.

*Choice of model*
I selected `eos4wt0` for the following reasons:
1. Relevance: Morgan Fingerprints are widely used in cheminformatics, capturing substructural patterns predictive of biological activity like liver toxicity.
2. Compatibility: The model accepts SMILES strings and outputs numerical vectors.


## Installation
1. Clone the Repository:
```bash
git clone <https://github.com/Mankavelda/outreachy-contributions>
cd outreachy contributions
```
2. Follow [this](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/installation) guide to install dependencies
3. Run the notebooks in order:

Data Inspection: `notebooks/02_data_inspection.ipynb`
Featurization: `notebooks/03_featurization.ipynb`




