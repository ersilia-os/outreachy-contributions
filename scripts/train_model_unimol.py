"""
Train and evaluate ML models using Uni-Mol features for drug permeability prediction.
Implements multiple models with cross-validation and detailed performance analysis.
"""

import os
import json
import logging
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_validate
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    precision_recall_curve, average_precision_score
)
import xgboost as xgb

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/model_training_unimol.log'),
        logging.StreamHandler()
    ]
)

def setup_directories():
    """Create necessary directories if they don't exist."""
    dirs = [
        'models/unimol',
        'data/results_unimol',
        'data/visualizations_unimol'
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def load_data():
    """Load features and labels for all splits.
    Converts log10 permeability (Y) to actual permeability in cm/s and creates
    binary labels using threshold of 8e-6 cm/s.
    """
    data = {}
    threshold = 8e-6  # Industry standard threshold in cm/s
    
    for split in ['train', 'valid', 'test']:
        # Load features
        features = np.load(f'data/features_unimol/caco2_{split}_features.npy')
        
        # Load labels and convert from log10 to actual permeability
        df = pd.read_csv(f'data/caco2_{split}.csv')
        permeability = np.power(10, df['Y'])  # Convert from log10 to actual values
        labels = (permeability >= threshold).astype(int)
        
        data[split] = {
            'features': features,
            'labels': labels,
            'df': df,
            'permeability': permeability  # Store actual permeability for analysis
        }
        
        logging.info(f"Loaded {split} set: {features.shape[0]} samples, {features.shape[1]} features")
    
    return data

def train_model(X_train, y_train, X_valid, y_valid):
    """Train XGBoost model with cross-validation and early stopping."""
    # Define model parameters
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'learning_rate': 0.01,
        'max_depth': 6,
        'min_child_weight': 1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'tree_method': 'hist',  # Faster histogram-based algorithm
        'random_state': 42
    }
    
    # Create DMatrix for faster training
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dvalid = xgb.DMatrix(X_valid, label=y_valid)
    
    # Set up evaluation list
    evallist = [(dtrain, 'train'), (dvalid, 'valid')]
    
    # Train model with early stopping
    num_round = 1000
    model = xgb.train(
        params,
        dtrain,
        num_round,
        evals=evallist,
        early_stopping_rounds=50,
        verbose_eval=100
    )
    
    return model

def plot_confusion_matrix(y_true, y_pred, title, save_path):
    """Plot and save confusion matrix."""
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d',
        cmap='Blues',
        xticklabels=['Low', 'High'],
        yticklabels=['Low', 'High']
    )
    plt.title(f'Confusion Matrix - {title}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_roc_curve(y_true, y_pred_proba, title, save_path):
    """Plot and save ROC curve."""
    from sklearn.metrics import roc_curve
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    auc = roc_auc_score(y_true, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {auc:.3f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {title}')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def evaluate_model(model, X, y, split_name):
    """Evaluate model performance and generate visualizations."""
    # Convert to DMatrix for prediction
    dtest = xgb.DMatrix(X, label=y)
    
    # Get predictions
    y_pred_proba = model.predict(dtest)
    y_pred = (y_pred_proba > 0.5).astype(int)
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y, y_pred),
        'precision': precision_score(y, y_pred),
        'recall': recall_score(y, y_pred),
        'f1': f1_score(y, y_pred),
        'roc_auc': roc_auc_score(y, y_pred_proba),
        'avg_precision': average_precision_score(y, y_pred_proba)
    }
    
    # Generate plots
    plot_confusion_matrix(
        y, y_pred,
        f'{split_name} Set',
        f'data/visualizations_unimol/confusion_matrix_{split_name}.png'
    )
    
    plot_roc_curve(
        y, y_pred_proba,
        f'{split_name} Set',
        f'data/visualizations_unimol/roc_curve_{split_name}.png'
    )
    
    return metrics

def main():
    """Main training and evaluation pipeline."""
    setup_directories()
    
    # Load data
    data = load_data()
    
    # Train model
    logging.info("Training XGBoost model...")
    model = train_model(
        data['train']['features'],
        data['train']['labels'],
        data['valid']['features'],
        data['valid']['labels']
    )
    
    # Save model
    model.save_model('models/unimol/xgboost_model.json')
    
    # Evaluate model
    results = {'xgboost': {}}
    logging.info("Evaluating model performance...")
    
    for split in ['train', 'valid', 'test']:
        logging.info(f"Evaluating {split} set...")
        results['xgboost'][split] = evaluate_model(
            model,
            data[split]['features'],
            data[split]['labels'],
            f'XGBoost_{split}'
        )
        logging.info(f"{split} set metrics: {results['xgboost'][split]}")
    
    # Save results
    with open('data/results_unimol/model_metrics.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    logging.info("Training and evaluation completed successfully!")

if __name__ == "__main__":
    main()
