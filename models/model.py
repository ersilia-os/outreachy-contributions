import os
import ast
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay, PrecisionRecallDisplay
import matplotlib.pyplot as plt

def parse_embedding(x):
    """
    Parse the string in x using ast.literal_eval.
    If the parsed value is a dict, try to extract a numeric embedding.
    First check for key "embedding"; if missing, check for "outcome".
    Otherwise, raise an error.
    """
    val = ast.literal_eval(x)
    if isinstance(val, dict):
        if "embedding" in val:
            return val["embedding"]
        elif "outcome" in val:
            return val["outcome"]
        else:
            raise ValueError(f"Expected a list of numeric values but got a dictionary without an embedding or outcome key: {val}")
    return val

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build a relative path to the data file (labels)
data_file = os.path.join(script_dir, '..', 'data', 'SARSCoV2_3CLPro_Diamond.csv')
df_labels = pd.read_csv(data_file, delimiter="\t")

# Load the features CSV
features_file = os.path.join(script_dir, '..', 'notebooks', 'features.csv')
df_features = pd.read_csv(features_file)

if len(df_labels) != len(df_features):
    raise ValueError("The number of rows in the labels file does not match the features file.")

# Map the target variable (Y) from df_labels into df_features
df_features['Y'] = df_labels['Y']

# Convert the "output" column entries using parse_embedding
X_list = df_features['output'].apply(parse_embedding)

# Convert the list of embeddings into a 2D NumPy array
try:
    X = np.stack(X_list.values)
except Exception as e:
    raise ValueError(f"Error converting embeddings into an array: {e}")

y = df_features['Y']

print("Shape of features (X):", X.shape)
print("First feature row:", X[0])
print("First few target values (y):")
print(y.head())

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model
preds = clf.predict(X_test)
preds_proba = clf.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, preds))
print("Classification Report:\n", classification_report(y_test, preds))
print("ROC-AUC:", roc_auc_score(y_test, preds_proba))

# Visualization
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# Confusion Matrix
ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test, ax=axs[0])
axs[0].set_title('Confusion Matrix')

# ROC Curve
RocCurveDisplay.from_estimator(clf, X_test, y_test, ax=axs[1])
axs[1].set_title('ROC Curve')

# Precision-Recall Curve
PrecisionRecallDisplay.from_estimator(clf, X_test, y_test, ax=axs[2])
axs[2].set_title('Precision-Recall Curve')

plt.tight_layout()
plt.show()