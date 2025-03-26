## 🧪 Week 2 Task – Dataset Preparation and Understanding (Ames, ADMET)

### 📌 Dataset Selection

As part of the Week 2 Outreachy contribution, I selected the **Ames dataset** from the **Therapeutics Data Commons (TDC)** which is specifically from the **ADMET Benchmark Group**. This dataset contains SMILES representations of molecules and their mutagenicity status based on the Ames test.

- **Benchmark Group**: `admet_group`
- **Dataset Name**: `ames`
- **Problem Type**: **Binary Classification**
- **Target Variable**: `Y`  
  - `1`: Mutagenic  
  - `0`: Non-mutagenic
- **Why This Dataset?**
  - It is lightweight & suitable for limited compute.
  - It is relevant for real-world drug discovery problem.
  - It directly supports binary classification workflows.
  - It is supported by TDC’s built-in dataset loader.

---

### ✅ Dataset Exploration and Preparation

Each compound in the dataset is represented by:
- `Drug_ID`: Unique identifier
- `Drug`: Molecular structure in SMILES format
- `Y`: Label (0 or 1)

The dataset was:
- Downloaded using `tdc.benchmark_group.admet_group()`
- Pre-split into `train_val` and `test` sets by the benchmark
- Further split into:
  - **Train**: 70%
  - **Validation**: 15% of `train_val`
  - **Test**: Remaining 15% (already provided)

Stratified splitting was applied using `scikit-learn` to preserve label balance.

---

### 📁 Files and Folder Structure

```bash
├── data/
│   ├── ames_train.csv   # Training data
│   ├── ames_val.csv     # Validation data
│   └── ames_test.csv    # Test data (from TDC)
├── notebooks/
│   └── 1_download_dataset.py  # Python script for dataset download & split

⚙️ How to Run This Script
📌 You must have Python 3.10+ and the required dependencies installed.

1. First create and activate a virtual environment
Always show details

```
python3.10 -m venv venv310
source venv310/bin/activate
```

2. Install dependencies
```
pip install PyTDC==0.3.5 scikit-learn==1.2.2 pandas
```
3. Run the dataset preparation script
```
python notebooks/1_download_dataset.py
```
4. Expected Output
✅ The script will download the Ames dataset from TDC.

✅ Apply stratified splitting.

✅ Save ames_train.csv, ames_val.csv, and ames_test.csv in the data/ folder.

✅ Print a sample preview of the training set.

🧠 Notes
Endpoint: Mutagenicity based on Ames test.

Feasibility: Dataset is small (~7,000 molecules) and processes quickly.

Preprocessing: No feature engineering yet but raw SMILES will be featurized in the next Step.