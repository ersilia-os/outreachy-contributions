"""
Analyze the generated molecular features in detail.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity


train_features = np.load('data/features/caco2_train_features.npy')
valid_features = np.load('data/features/caco2_valid_features.npy')
test_features = np.load('data/features/caco2_test_features.npy')


train_df = pd.read_csv('data/processed/caco2_train.csv')
valid_df = pd.read_csv('data/processed/caco2_valid.csv')
test_df = pd.read_csv('data/processed/caco2_test.csv')

print("\nFeature Analysis:")
print("-" * 50)


for name, features in [('Train', train_features), ('Valid', valid_features), ('Test', test_features)]:
    print(f"\n{name} Set:")
    print(f"Shape: {features.shape}")
    print(f"Active bits (mean): {features.mean():.3f}")
    print(f"Sparsity: {(features == 0).mean():.3f}")
    
    
    bit_freq = features.mean(axis=0)
    print(f"Most common bits: {np.sort(bit_freq)[-5:]}")
    print(f"Least common bits: {np.sort(bit_freq)[:5]}")


print("\nSimilarity Analysis:")
print("-" * 50)

def analyze_similarities(features, labels):
    n_samples = min(100, len(features))
    subset_idx = np.random.choice(len(features), n_samples, replace=False)
    subset_features = features[subset_idx]
    subset_labels = labels[subset_idx]
    
    sims = cosine_similarity(subset_features)
    
    same_class = []
    diff_class = []
    
    for i in range(n_samples):
        for j in range(i+1, n_samples):
            sim = sims[i,j]
            if subset_labels[i] == subset_labels[j]:
                same_class.append(sim)
            else:
                diff_class.append(sim)
    
    return {
        'same_class_mean': np.mean(same_class),
        'diff_class_mean': np.mean(diff_class),
        'overall_mean': np.mean(sims[np.triu_indices_from(sims, k=1)])
    }

for name, features, df in [('Train', train_features, train_df), 
                         ('Valid', valid_features, valid_df),
                         ('Test', test_features, test_df)]:
    print(f"\n{name} Set:")
    sim_stats = analyze_similarities(features, df['Binary'].values)
    print(f"Mean similarity (same class): {sim_stats['same_class_mean']:.3f}")
    print(f"Mean similarity (diff class): {sim_stats['diff_class_mean']:.3f}")
    print(f"Overall mean similarity: {sim_stats['overall_mean']:.3f}")


plt.figure(figsize=(10, 6))
plt.hist(train_features.mean(axis=0), bins=50)
plt.title('Distribution of Bit Frequencies in Training Set')
plt.xlabel('Frequency')
plt.ylabel('Count')
plt.savefig('data/visualizations/bit_frequency_dist.png')
plt.close()
