from ersilia import ErsiliaModel
import os

def featurize_data(model_id, datasets):
    model = ErsiliaModel(model=model_id)
    model.serve()

    for input_file, output_file in datasets.items():
        if os.path.exists(input_file):
            model.run(input=input_file, output=output_file)
        else:
            raise FileNotFoundError(f"Input file '{input_file}' not found!")

if __name__ == "__main__":
    model_id = "eos8a4x"  # Replace with actual model ID

    datasets = {
        "data/bbbp_train.csv": "data/bbbp_train_featurised.csv",
        "data/bbbp_test.csv": "data/bbbp_test_featurised.csv",
        "data/bbbp_valid.csv": "data/bbbp_valid_featurised.csv",
    }

    featurize_data(model_id, datasets)
