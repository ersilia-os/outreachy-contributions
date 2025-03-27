# Drug Absorption Prediction Model 🧬

## Project Overview 🎯
This project develops a machine learning model to predict drug absorption using the Caco2_Wang dataset from Therapeutics Data Commons (TDC). Our goal is to create a binary classifier that predicts whether a drug compound will have high or low permeability through the Caco2 cell membrane.

### 📊 Dataset Significance
The Caco2_Wang dataset is crucial for drug discovery:

| Feature | Description |
|---------|-------------|
| Cell Model | Caco2 cells from human colorectal adenocarcinoma - established intestinal absorption model |
| Measurements | Actual permeability in cm/s - directly relevant to drug development |
| Data Quality | Well-balanced (51.6% low vs 48.4% high permeability), 910 compounds |

## Understanding the Data

### Experimental Background
- **Original Task Type**: Regression (predicting exact permeability values)
- **Measurement**: Permeability through Caco2 cell monolayers (human intestinal model)
- **Units**: Centimeters per second (cm/s)
- **Value Range**: 1.74 × 10⁻⁸ to 3.09 × 10⁻⁴ cm/s

### Conversion to Binary Classification
While the Caco2_Wang dataset originally provides continuous permeability values (regression task), I converted it to a binary classification problem using industry-standard thresholds:

- **Cutoff Value**: 8 × 10⁻⁶ cm/s (based on FDA guidelines and literature)
- **Binary Labels**:
  - High Permeability (1): ≥ 8 × 10⁻⁶ cm/s
  - Low Permeability (0): < 8 × 10⁻⁶ cm/s

**Rationale for Conversion**:
1. Binary classification models are often more robust and easier to validate
2. The cutoff value (8 × 10⁻⁶ cm/s) is well-established in pharmaceutical research
3. In drug discovery, the binary high/low permeability classification is often more actionable than exact values

### 📈 Dataset Composition

| Split | Size | Low Permeability | High Permeability |
|-------|------|------------------|-------------------|
| Total | 910 | 51.6% | 48.4% |
| Training | 637 | 51.6% | 48.4% |
| Validation | 91 | 46.2% | 53.8% |
| Test | 182 | 54.4% | 45.6% |

### Molecular Properties
- **Input Format**: SMILES strings (molecular structure)
- **Complexity**: Average SMILES length ~60 characters
- **Chemistry**: Primarily organic compounds
  - Carbon (~57%)
  - Oxygen (~20%)
  - Nitrogen (~10%)
  - Hydrogen (~9%)
  - Other elements (~4%)

## 📂 Project Structure

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `data/` | Dataset files | - `caco2_train.csv` (637 compounds)<br>- `caco2_valid.csv` (91 compounds)<br>- `caco2_test.csv` (182 compounds)<br>- `dataset_summary.md` |
| `notebooks/` | Analysis | Jupyter notebooks |
| `scripts/` | Core code | Python implementation files |
| `models/` | Checkpoints | Saved model states |
| Root | Configuration | - `requirements.txt`<br>- `README.md` |

## Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Create and Activate Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate it on Linux/Mac
source venv/bin/activate

# Or on Windows
venv\Scripts\activate
```

2. **Install Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt
```

## Usage Guide

### 1. Dataset Preparation
```bash
# Download and split the dataset
python download_dataset.py
```
This will:
- Download the Caco2_Wang dataset from TDC
- Split it into train/validation/test sets
- Save the splits in the `data` directory
- Generate a detailed analysis in `data/dataset_summary.md`

### 2. Data Exploration
```bash
# View dataset statistics and visualizations
python explore_dataset.py
```
This will:
- Generate detailed statistics about the dataset
- Create visualizations in the `data` directory

### 3. Molecular Featurization

#### 🛠️ Implementation Journey

#### 1. Uni-Mol Model Implementation
**Initial Approach**
- Selected Ersilia's Uni-Mol model (eos39co) for:
  - 3D molecular information capture
  - Large-scale training (>200M conformations)
  - SE(3) equivariant architecture

**Challenges & Solutions**
| Challenge | Solution |
|-----------|----------|
| Docker Hub connectivity | Implemented proper TLS handling |
| Resource limitations | Docker pruning for optimization |
| Permission issues | Elevated necessary privileges |

**Current Status**
```bash
# Generate molecular features
python scripts/featurize_data_unimol.py
```

**Output Location**
- Script: `scripts/featurize_data_unimol.py`
- Features: `data/features_unimol/`
- Statistics: `data/features_unimol/featurization_stats.json`
- Logs: `data/visualizations/featurization.log`

**Uni-Mol Model Analysis**

| Aspect | Details |
|--------|----------|
| Architecture | SE(3)-equivariant transformer network |
| Training Data | >200M molecular conformations |
| Input | 3D molecular conformers |
| Output | Continuous vector embeddings |

*Feature Characteristics*
| Metric | Description |
|--------|-------------|
| Dimension | Fixed-length continuous vectors |
| Information | Global molecular properties + 3D structure |
| Validation | Strict dimension and value checks |
| Quality Checks | - NaN threshold: 1%<br>- Infinite threshold: 1%<br>- Zero threshold: 95% |

*Key Advantages*
| Feature | Benefit |
|---------|----------|
| 3D Information | Captures conformational properties |
| Global Context | Models long-range atomic interactions |
| Learned Features | Adapts to chemical patterns |
| Robustness | Multiple embedding extraction paths |

*Performance Characteristics*
| Metric | Value |
|--------|-------|
| Processing | Batch-based (32 molecules/batch) |
| Error Handling | Comprehensive with detailed logging |
| Validation | Dimension and statistical checks |
| Recovery | Multiple fallback paths for embeddings |

    
#### 2. Morgan Fingerprints Implementation
**Alternative Approach**
| Feature | Benefit |
|---------|----------|
| Dependencies | Built into RDKit - no external requirements |
| Performance | ~910 molecules/10 seconds |
| Reliability | Industry standard in drug discovery |
| Success Rate | 100% feature generation |


```bash
# Generate molecular features
python scripts/featurize_data.py
```

This script performs several key tasks:
1. **Data Loading**: Reads SMILES strings from each dataset split
2. **Feature Generation**: Creates 2048-bit Morgan fingerprints
3. **Validation**: Checks feature quality and computes statistics
4. **Visualization**: Creates PCA plots to visualize chemical space
5. **Error Handling**: Tracks and reports any failed molecules

### 📋 Feature Analysis

#### 1. Feature Properties
| Metric | Value |
|--------|-------|
| Dimensionality | 2048 binary bits/molecule |
| Sparsity | 96.7-96.9% zeros |
| Active Bits | 3.1-3.3% per molecule |
| Common Substructures | 75-95% presence |
| Data Quality | No NaN/infinite values |

#### 2. Chemical Space Analysis
| Analysis | Results |
|----------|----------|
| PCA Variance | 3.3-5.2% (first 2 PCs) |
| Complexity | High (low explained variance) |
| Tanimoto Similarity | 0.149-0.163 average |
| Chemical Diversity | High (low similarity scores) |

#### 3. Performance Metrics
| Metric | Value |
|--------|-------|
| Speed | 400-600 molecules/second |
| Memory | <1GB RAM usage |
| Success Rate | 100% (910/910) |
| Parse Errors | None |

#### 4. ML Advantages
| Feature | Benefit |
|---------|----------|
| Format | Fixed-length vectors |
| Interpretability | Each bit = specific substructure |
| Efficiency | Sparse binary storage |
| Compatibility | Works with most ML algorithms |

#### Output Structure

```
data/
├── features/
│   ├── caco2_train_features.npy   # Training set feature vectors
│   ├── caco2_valid_features.npy   # Validation set feature vectors
│   ├── caco2_test_features.npy    # Test set feature vectors
│   └── featurization_stats.json   # Detailed statistics about the process
├── processed/
│   ├── caco2_train.csv           # Processed training data
│   ├── caco2_valid.csv           # Processed validation data
│   └── caco2_test.csv            # Processed test data
├── visualizations/
│   ├── pca_features_train.png    # PCA plot for training set
│   ├── pca_features_valid.png    # PCA plot for validation set
│   ├── pca_features_test.png     # PCA plot for test set
│   └── bit_frequency_dist.png    # Distribution of Morgan fingerprint bits
└── featurization.log            # Detailed process log

```

#### Feature Statistics
The `featurization_stats.json` file contains detailed statistics about the generated features:

1. **Overall Statistics**
   - Total molecules processed: 910
   - Successful molecules: 910
   - Success rate: 100%

2. **Split-wise Statistics**
   - Training set (637 molecules):
     - Mean active bits: 3.34%
     - Standard deviation: 0.180
     - Zero bits: 1,260,954 (96.7%)
   - Validation set (91 molecules):
     - Mean active bits: 3.11%
     - Standard deviation: 0.174
     - Zero bits: 180,563 (96.9%)
   - Test set (182 molecules):
     - Mean active bits: 3.11%
     - Standard deviation: 0.174
     - Zero bits: 361,153 (96.9%)

#### Visualizations
The visualization files provide insights into the feature space:

1. **PCA Plots** (`pca_features_*.png`)
   - 2D projection of 2048-dimensional fingerprints
   - Color-coded by permeability class (high/low)
   - Explained variance ratios (3.3-5.2%)
   - Shows molecular similarity patterns

2. **Bit Distribution** (`bit_frequency_dist.png`)
   - Distribution of Morgan fingerprint bits
   - Shows sparsity of the representation
   - Identifies common molecular substructures

3. **Process Log** (`featurization.log`)
   - Detailed timing information
   - Error tracking and handling
   - Feature validation results



## Technical Details

### 📑 Data Format

| Field | Description |
|-------|-------------|
| `Drug_ID` | Unique compound identifier |
| `Drug` | SMILES string (molecular structure) |
| `Y` | log10(permeability) in cm/s |
| `Permeability` | Actual permeability (10^Y cm/s) |
| `Binary` | 0: low, 1: high permeability |

### 🧬 SMILES Format

| Aspect | Details |
|--------|----------|
| Format | Text representation of molecular structure |
| Length | ~60 characters average |
| Example | `CC(=O)NC1=CC=C(O)C=C1` (Acetaminophen) |
| Elements | C, O, N, H (>95% of atoms) |

### 🎓 Data Quality

#### Class Distribution
| Split | Low Permeability | High Permeability |
|-------|------------------|-------------------|
| Overall | 51.6% | 48.4% |
| Training | 51.6% | 48.4% |
| Validation | 46.2% | 53.8% |
| Test | 54.4% | 45.6% |

#### Value Statistics
| Metric | Value |
|--------|-------|
| Range | 1.74 × 10⁻⁸ to 3.09 × 10⁻⁴ cm/s |
| Median | 7.39 × 10⁻⁶ cm/s |
| Distribution | See `data/permeability_distribution.png` |

