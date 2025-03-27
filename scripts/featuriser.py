import os
import subprocess
import time
import pandas as pd

def featuriser(model_id):
    print(f"Fetching model {model_id}...")
    fetch_result = subprocess.run(["ersilia", "fetch", model_id], capture_output=True, text=True)
    if fetch_result.returncode != 0:
        print(f" Error fetching model: {fetch_result.stderr}")
        return None  
    print("Model fetched successfully")

    server_process = subprocess.run(["ersilia", "serve", model_id])
    time.sleep(15)
    print("Ersilia model server is running")

    files = [
        ("../data/train.csv", "../data/featurised_train.csv"),
        ("../data/valid.csv", "../data/featurised_valid.csv"),
        ("../data/test.csv", "../data/featurised_test.csv"),
    ]

    for input_file, output_file in files:
        print(f"Processing {input_file}...")

        # Load dataset
        df = pd.read_csv(input_file)
        print(f"Featurizing Drug1 from {input_file}...")
        df_drug1 = df[['Drug1']].rename(columns={'Drug1': 'SMILES'})  # Rename column to "SMILES" for Ersilia
        drug1_input = input_file.replace(".csv", "_drug1.csv")
        drug1_output = input_file.replace(".csv", "_drug1_feat.csv")
        df_drug1.to_csv(drug1_input, index=False)

        result_drg1 = subprocess.run(["ersilia", "run", "-i", drug1_input, "-o", drug1_output], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result_drg1.returncode != 0:
            print(f"Error featurizing Drug1 in {input_file}:", result_drg1.stderr)
            continue 
        else:
            print(f"Successfully featurized Drug1 in {input_file}")

        df_drug1_feat = pd.read_csv(drug1_output)
        df_drug1_feat = df_drug1_feat.add_prefix("Drug1_")  

     
        print(f"Featurizing Drug2 from {input_file}...")
        df_drug2 = df[['Drug2']].rename(columns={'Drug2': 'SMILES'})
        drug2_input = input_file.replace(".csv", "_drug2.csv")
        drug2_output = input_file.replace(".csv", "_drug2_feat.csv")
        df_drug2.to_csv(drug2_input, index=False)
        result_drg2 = subprocess.run(["ersilia", "run", "-i", drug2_input, "-o", drug2_output], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result_drg2.returncode != 0:
            print(f"Error featurizing Drug2 in {input_file}:", result_drg2.stderr)
            continue  # Skip to next dataset if error occurs
        else:
            print(f"Successfully featurized Drug2 in {input_file}")

        # Load featurized Drug2 data
        df_drug2_feat = pd.read_csv(drug2_output)
        df_drug2_feat = df_drug2_feat.add_prefix("Drug2_")  # Prefix columns

        df_final = pd.concat([df, df_drug1_feat, df_drug2_feat], axis=1)

        # Drop original Drug1 & Drug2 columns (optional)
        df_final.drop(columns=["Drug1", "Drug2"], inplace=True)

        # Save the final featurized dataset
        df_final.to_csv(output_file, index=False)
        print(f"Featurized data saved to {output_file}")

        
    delete_temp_files()

    # Stop the Ersilia server
    print("Ersilia server stopped.")

def delete_temp_files():
    temp_files = glob.glob("../data/*_drug1.csv") + glob.glob("../data/*_drug1_feat.csv") + \
                 glob.glob("../data/*_drug2.csv") + glob.glob("../data/*_drug2_feat.csv")
    
    for file in temp_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")



featuriser("eos4wt0")
