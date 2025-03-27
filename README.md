# **Blood Brain Barrier (BBB) Permeability Prediction**  

This project is part of the **Outreachy contribution period**, where I explore how AI/ML can help predict if molecules can cross the **Blood Brain Barrier (BBB)**.  


## Project Checklist  

[ ] **Select a dataset** – Choose a dataset that helps understand drug permeability in the Blood Brain Barrier.  
[ ] **Load and explore the data** – Open and inspect the data to understand its structure.  
[ ] **Automate data loading** – Create scripts to load the data automatically.  
[ ] **Automate data exploration** – Write scripts to summarize and visualize the dataset.  
[ ] **Choose a featurizer** – Pick a method to convert molecules into useful numerical features.  
[ ] **Automate featurization** – Develop scripts to apply featurization on all drug molecules.  
[ ] **Build an automation pipeline** – Combine all steps into a seamless, automated workflow.  

---

## **Project Structure**  

```
/project-root
│── data/                # Raw & processed datasets
│── notebooks/           # Jupyter Notebooks for testing
│── scripts/             # Automation scripts
│── figures/             # Visualization Picture
│── models/              # Model checkpoints (to be added)
│── README.md            # This file
│── requirements.txt     # Dependencies
```

---

## **Project Breakdown**  

### **Choosing the Dataset**  

The **Blood Brain Barrier (BBB) dataset** was chosen because:  
✔ The **Blood Brain Barrier (BBB)** is like a security guard for the brain, blocking harmful substances. But sometimes, it also blocks helpful drugs. By predicting which drugs can cross it, we can improve treatments for brain diseases like **meningitis, stroke, and epilepsy**, which are common in Nigeria.  

---

### **Loading the Data**  

 **Automated Script:** `scripts/data_loader.py`  

```python
from scripts.data_loader import Dataloader
from scripts.eda import ExploratoryDataAnalysis
from scripts.featurise import FeatureExtractor

# Initialize data loader and fetch dataset
data_loader = Dataloader()
data, df, splits= data_loader.fetch_bbb_dataset()
```

---

### **Exploring the Data**  
  
 **Automated Script:** `scripts/eda.py`  

```python
# Label Distribution (0 = Non-permeable, 1 = Permeable)
    plt.figure(figsize=(6, 4))
    sns.countplot(x=df["Y"], palette="coolwarm")
    plt.xlabel("BBB Permeability (0 = No, 1 = Yes)")
    plt.ylabel("Count")
    plt.title("Label Distribution - Blood Brain Barrier Permeability")
    plt.savefig(os.path.join(self.figure_dir, "label_distribution.png"))
    plt.close()
    self.logger.info("Label distribution saved.")       
```

---

### **Featurizing the Data**  

To understand if a drug can cross the **Blood Brain Barrier**, we need to look at its properties—like size, weight, and how it dissolves. I used **RDKit’s physicochemical descriptors** because they give a clear picture of a drug’s behavior. Instead of guessing, this method helps make sure the right drugs reach the brain, giving hope for better treatments for diseases like **meningitis, epilepsy, and stroke** in Nigeria. 
  
**Automated Script:** `scripts/featurise.py`  

```python
# Fetch model if not already available
self.logger.info(" Fetching RDKit descriptors model from Ersilia...")
fetch_output = self.run_command(f"ersilia -v fetch {ERSILIA_DESCRIPTORS}")
if fetch_output is None:
    self.logger.error(" Failed to fetch the model.")
    return None

# Serve the model
self.logger.info(" Serving the model in the background...")
serve_output = self.run_command(f"ersilia -v serve {ERSILIA_DESCRIPTORS}")
if serve_output is None:
    self.logger.error(" Failed to serve the model.")
    return None
    }
```

---

### **Automating the Entire Process**  

Instead of running each script manually, I **automated everything** with a single pipeline script.  

**Main Automation Script:** `scripts/main.py`  

```python

    # Step 1: Download dataset if not present
    if not os.path.exists(DATA_PATH):
        logger.info("Dataset not found. Downloading now...")
        downloader = Dataloader()
        downloader.download_data()
    else:
        logger.info("Dataset found. Skipping download.")

    # Step 2: Perform Exploratory Data Analysis
    logger.info("Running Exploratory Data Analysis...")
    eda = ExploratoryDataAnalysis()
    eda.generate_visuals()

    # Step 3: Extract Features using Ersilia CLI
    if not os.path.exists(FEATURES_PATH):
        logger.info("Extracting molecular descriptors...")
        extractor = FeatureExtractor()
        extractor.generate_features()
    else:
        logger.info("Feature extraction already done. Skipping.")

    logger.info("Pipeline completed successfully!")
```

To run everything at once:  
```bash
python scripts/pipeline.py
```

---

## **How to run my Code**  
**Install Conda ana Ersilia:** 
```bash
conda create --name ersilia python=3.12 -y
conda activate ersilia
```
**Clone the repo:**  
```bash
git clone https://github.com/AmarachOrdor18/outreachy-contributions.git
cd Outreachy-contributions
```

### **Run the full pipeline:**  
```bash
python scripts/main.py
```

### **Run Jupyter notebooks (if needed):**  
```bash
jupyter notebook
```

---

## **Why This Matters**  

Predicting **Blood Brain Barrier permeability** is a huge deal in drug development. This project helps automate the process, making it easier to find promising drug candidates **faster** and **cheaper** than traditional lab tests.  