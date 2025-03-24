# Download and load dataset into memory


from tdc.single_pred import ADME
data = ADME(name = 'Bioavailability_Ma')
df = data.get_data()

# Set paths for saving data, .tab saves by default in the working directory

csv_path = "../data/bioavailability.csv"

# Save dataset
df.to_csv(csv_path, index=False)

print(f"Data saved successfully")
