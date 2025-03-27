import logging, os, glob
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from eosce.models import ErsiliaCompoundEmbeddings

load_dotenv()

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

if not (LOCAL_DATA_PATH := os.environ.get("LOCAL_DATA_PATH")):
    raise ValueError("LOCAL_DATA_PATH environment variable is not set.")

if not (SMILES_FEATURE_COLUMN := os.environ.get("SMILES_FEATURE_COLUMN")):
    raise ValueError("SMILES_FEATURE_COLUMN environment variable is not set.")

# init model once to avoid reloading for each dataframe record
model = ErsiliaCompoundEmbeddings()


# Function to compute descriptors for a batch of SMILES
def compute_descriptors(smiles_list: list) -> np.ndarray:
    try:
        embeddings = model.transform(smiles_list)
        return embeddings
    except Exception as e:
        logging.error(f"could not compute descriptors: {e}")


# Process CSV in batches
def preprocess_data(
    input_file: Path, smiles_column: str, data_store_path: Path, batch_size: int = 2000
) -> None:
    """Utility to featurize given CSV files using the Ersilia Compound Embeddings model to produce
        embeddings of 1024 features for small molecules

        for more details visit:
        https://github.com/ersilia-os/eos2gw4

    Args:
        input_file (Path): path to raw csv file
        smiles_column (str): column with SMILE compound or molecule
        data_store_path (Path): path to save featurized data
        batch_size (int, optional): number of records to process at a time. Defaults to 2000.
    """
    try:
        batch_num = 1
        for chunk in pd.read_csv(input_file, chunksize=batch_size):

            # drop any rows with missing SMILES string
            chunk = chunk.dropna(subset=[smiles_column])
            smiles_list = chunk[smiles_column].tolist()

            # Compute descriptors
            descriptors = compute_descriptors(smiles_list)
            ersilia_descriptors = np.vstack(descriptors)
            descriptor_df = pd.DataFrame(
                ersilia_descriptors,
                columns=[f"desc_{i}" for i in range(ersilia_descriptors.shape[1])],
                index=chunk.index,
            )

            # merge and drop unnecessary columns
            chunk.drop(columns=[smiles_column], inplace=True)
            chunk = pd.concat([chunk, descriptor_df], axis=1)
            os.makedirs(data_store_path, exist_ok=True)
            chunk.to_parquet(
                os.path.join(
                    data_store_path,
                    f"featurised_{os.path.splitext(os.path.basename(input_file))[0]}.parquet",
                ),
                engine="pyarrow",
                compression="zstd",
                index=False,
            )
            logging.info(f"Batch {batch_num} processed and saved.")
            batch_num += 1

        logging.info(f"All batches processed. Data saved to {data_store_path} 🚀")
    except Exception as e:
        logging.error(f"could not preprocess data ⚠️ --> {e}")


if __name__ == "__main__":
    for file_path in glob.glob(os.path.join(LOCAL_DATA_PATH + "/raw", "*.csv")):
        store_path = LOCAL_DATA_PATH + "/featurized"
        preprocess_data(file_path, smiles_column=SMILES_FEATURE_COLUMN, data_store_path=store_path)
