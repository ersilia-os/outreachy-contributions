from tdc.single_pred import ADME
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

# Load dataset
data = ADME(name='Caco2_Wang')
df_full = data.get_data()

# Convert permeability from log scale to actual values and apply cutoff
CUTOFF = 8e-6  # 8 × 10⁻⁶ cm/s standard cutoff
df_full['Permeability'] = 10 ** df_full['Y']  # Convert from log10 to actual values
df_full['Binary'] = (df_full['Permeability'] >= CUTOFF).astype(int)

# Plot permeability distribution
plt.figure(figsize=(10, 6))
plt.hist(df_full['Y'], bins=30, edgecolor='black')
plt.axvline(x=np.log10(CUTOFF), color='r', linestyle='--', label=f'Cutoff: {CUTOFF:.1e} cm/s')
plt.xlabel('Log10(Permeability) [cm/s]')
plt.ylabel('Number of Compounds')
plt.title('Distribution of Caco2 Permeability Values')
plt.legend()
plt.savefig('data/permeability_distribution.png')
plt.close()

print("=== Full Dataset Analysis ===")
print(f"Total compounds: {len(df_full)}")
print(f"\nPermeability Statistics (cm/s):")
print(f"Minimum: {df_full['Permeability'].min():.2e}")
print(f"Maximum: {df_full['Permeability'].max():.2e}")
print(f"Mean: {df_full['Permeability'].mean():.2e}")
print(f"Median: {df_full['Permeability'].median():.2e}")

print(f"\nBinary Classification (cutoff = {CUTOFF:.1e} cm/s):")
print(f"Low permeability: {(df_full['Binary'] == 0).sum()} compounds ({(df_full['Binary'] == 0).mean()*100:.1f}%)")
print(f"High permeability: {(df_full['Binary'] == 1).sum()} compounds ({(df_full['Binary'] == 1).mean()*100:.1f}%)\n")

# Get splits and add binary labels
split = data.get_split()
for name in split:
    split[name]['Permeability'] = 10 ** split[name]['Y']
    split[name]['Binary'] = (split[name]['Permeability'] >= CUTOFF).astype(int)

def analyze_set(df, name):
    print(f"\n=== {name} Set Analysis ===")
    print(f"Number of compounds: {len(df)}")
    
    # Label distribution
    low_perm = (df['Binary'] == 0).sum()
    high_perm = (df['Binary'] == 1).sum()
    print(f"\nLabel Distribution:")
    print(f"Low permeability (0): {low_perm} compounds ({low_perm/len(df)*100:.1f}%)")
    print(f"High permeability (1): {high_perm} compounds ({high_perm/len(df)*100:.1f}%)")
    
    # Permeability statistics
    print(f"\nPermeability Statistics (cm/s):")
    print(f"Minimum: {df['Permeability'].min():.2e}")
    print(f"Maximum: {df['Permeability'].max():.2e}")
    print(f"Mean: {df['Permeability'].mean():.2e}")
    print(f"Median: {df['Permeability'].median():.2e}")
    
    # SMILES analysis
    smiles = df['Drug']
    lengths = [len(s) for s in smiles]
    print(f"\nMolecular Complexity (SMILES length):")
    print(f"Min length: {min(lengths)}")
    print(f"Max length: {max(lengths)}")
    print(f"Average length: {np.mean(lengths):.1f}")
    
    # Most common elements (first character of each atom symbol)
    elements = []
    for smile in smiles:
        # Basic element extraction (this is a simplification)
        els = [c for c in smile if c.isupper()]
        elements.extend(els)
    
    top_elements = Counter(elements).most_common(5)
    print(f"\nTop 5 Elements:")
    for element, count in top_elements:
        print(f"{element}: {count} occurrences ({count/len(elements)*100:.1f}%)")

# Analyze each set
for split_name, df in split.items():
    analyze_set(df, split_name.capitalize())

# Save summary to a markdown file
with open('data/dataset_summary.md', 'w') as f:
    f.write("# Caco2_Wang Dataset Analysis\n\n")
    
    f.write("## Dataset Background\n")
    f.write("The Caco2_Wang dataset contains experimental measurements of drug permeability through Caco2 cells, ")
    f.write("which are widely used as a model for human intestinal absorption. The permeability values are measured ")
    f.write("in centimeters per second (cm/s) and are typically reported in log scale.\n\n")
    
    f.write("### Binarization Approach\n")
    f.write(f"Following industry standards, we use a cutoff of {CUTOFF:.1e} cm/s to classify compounds:\n")
    f.write("- Values ≥ 8 × 10⁻⁶ cm/s are considered **high permeability** (1)\n")
    f.write("- Values < 8 × 10⁻⁶ cm/s are considered **low permeability** (0)\n\n")
    
    f.write("## Dataset Statistics\n")
    f.write(f"Total compounds: {len(df_full)}\n\n")
    f.write("### Permeability Distribution\n")
    f.write(f"- Minimum: {df_full['Permeability'].min():.2e} cm/s\n")
    f.write(f"- Maximum: {df_full['Permeability'].max():.2e} cm/s\n")
    f.write(f"- Mean: {df_full['Permeability'].mean():.2e} cm/s\n")
    f.write(f"- Median: {df_full['Permeability'].median():.2e} cm/s\n\n")
    
    f.write("### Class Distribution\n")
    low = (df_full['Binary'] == 0).sum()
    high = (df_full['Binary'] == 1).sum()
    f.write(f"- Low permeability: {low} compounds ({low/len(df_full)*100:.1f}%)\n")
    f.write(f"- High permeability: {high} compounds ({high/len(df_full)*100:.1f}%)\n\n")
    
    f.write("### Data Splits\n")
    for split_name, df in split.items():
        f.write(f"#### {split_name.capitalize()} Set\n")
        f.write(f"- Size: {len(df)} compounds\n")
        low = (df['Binary'] == 0).sum()
        high = (df['Binary'] == 1).sum()
        f.write(f"- Low permeability: {low} compounds ({low/len(df)*100:.1f}%)\n")
        f.write(f"- High permeability: {high} compounds ({high/len(df)*100:.1f}%)\n\n")
    
    f.write("### Molecular Composition\n")
    f.write("The dataset contains organic molecules with the following characteristics:\n")
    for split_name, df in split.items():
        smiles = df['Drug']
        lengths = [len(s) for s in smiles]
        elements = []
        for smile in smiles:
            els = [c for c in smile if c.isupper()]
            elements.extend(els)
        top_elements = Counter(elements).most_common(5)
        
        f.write(f"\n#### {split_name.capitalize()} Set\n")
        f.write(f"- SMILES length: min={min(lengths)}, max={max(lengths)}, mean={np.mean(lengths):.1f}\n")
        f.write("- Most common elements:\n")
        for element, count in top_elements:
            f.write(f"  - {element}: {count} occurrences ({count/len(elements)*100:.1f}%)\n")
    
    f.write("\n## Visualization\n")
    f.write("![Permeability Distribution](permeability_distribution.png)\n")
    f.write("\nThe histogram shows the distribution of permeability values in log scale. ")
    f.write("The red dashed line indicates the cutoff value used for binary classification.")

print("\nDetailed analysis has been saved to data/dataset_summary.md")
