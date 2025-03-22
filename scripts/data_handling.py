# Download and load dataset into memory

from tdc.single_pred import Epitope
data = Epitope(name = 'PDB_Jespersen')
df = data.get_data()

# Set paths for saving data, .pkl saves by default in the working directory

csv_path = "../data/raw_pdb_jespersen.csv"
pkl_path = "../data/pdb_jesperson.pkl"

# Save dataset
df.to_csv(csv_path, index=False)
df.to_pickle(pkl_path)

print(f"Data saved successfully")
