from tdc.single_pred import ADME
import pandas as pd

data = ADME(name = 'BBB_Martins')
split = data.get_split()

for split_name, df in split.items():
    df = pd.DataFrame(df)  # Convert to Pandas DataFrame
    file_path = f"data/bbbp_{split_name}.csv"
    df.to_csv(file_path, index=False)