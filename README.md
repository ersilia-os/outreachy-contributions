# Outreachy contribution period

# **Dataset of Interest : Blood-Brain Barrier (BBB) - Martins et al Dataset**

## 📌 **Dataset Overview**
The Blood-Brain Barrier (BBB) is a selective membrane that restricts most foreign substances, including drugs, from entering the brain. This dataset, **BBB_Martins**, provides insights into drug permeability across the BBB, helping researchers design effective central nervous system (CNS) drugs.

This dataset is crucial for developing treatments for neurological disorders such as Alzheimer’s, Parkinson’s, and brain cancer, where drug permeability is a key challenge.

The dataset was downloaded using Python and the Therapeutics Data Commons (TDC) library. I created a script that helps me to fetch the data and save it in the data folder.

### **Dataset Analysis:** 

This dataset is a binary classification task, where the goal is to predict the activity of BBB against a drug. It is positive when Y=1 and negative when Y=0.

**Features:**

Drug_ID: Assigns a reference ID to each drug

Drug : SMILES representation.

(Y): Indicates BBB penetration status  (0 or 1) explicitly provided for each compound.

**Class Distribution:**

Total Samples: 2030
Y=1: 1551 drugs (76.4% of the dataset).
Y=0: 479 drugs (23.59% of the dataset).

---

This dataset serves as a valuable resource for training machine learning models to predict BBB permeability based on molecular properties. The dataset is sufficient enough to support robust model training while remaining computationally feasible for most modern machine learning frameworks. More processes can be done during training the model to achieve great results.

## 📂 **Project Structure**
```
├── data
│   ├── BBB_Martins
│   │   ├── BBB_Martins.csv  # Complete dataset
│   │   ├── train.csv        # Training split
│   │   ├── test.csv         # Testing split
│   │   ├── valid.csv        # Validation split
│ 
│
├── models                   # Placeholder for models
│
├── notebooks
│   ├── analysis.ipynb       # Main notebook for visualization and analysis
│
├── scripts
│   ├── run.py               # Script to preprocess data and prepare for analysis
│
├── .gitignore
├── LICENSE
├── README.md               
```

---
## 🛠 **Setup**
To get started, follow these steps:

### **Clone the Repository**
```bash
git clone https://github.com/jaycobson/outreachy-contributions.git
cd outreachy-contributions
```

---
## 🚀 **How to Use**

### **Step 1: Run the Data Processing Script**
Navigate to the `scripts/` folder and run `run.py` to preprocess the data:
```bash
python scripts/run.py
```

### **Step 2: Open and Run the Analysis Notebook**
Once the data is processed, open the Analysis Jupyter Notebook for visualization and analysis:

Run all the cells to see the **data visualizations, drug distribution analysis and predictive modeling insights**.

---
## 📊 **Key Features of the Analysis Notebook**
- **Visualizing Drug Distributions**: Count plots of drug occurrence.
- **Molecular Structure Representation**: Visualizing drug molecules using RDKit.
- **Checking for Duplicates**: Identifying and handling duplicate entries.

