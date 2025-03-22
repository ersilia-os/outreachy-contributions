import pandas as pd

class Preprocessor:
    def __init__(self, gdsc_df, benchmark_df):
        self.gdsc_df = gdsc_df
        self.benchmark_df = benchmark_df        

    def preprocess_data(self):
        """
        Preprocesses the dataset by renaming columns.
        """
        try:
            if self.benchmark_df is None or not isinstance(self.benchmark_df, pd.DataFrame):
                raise ValueError("Invalid input: Expected a DataFrame but received None or incorrect type.")

            column_mapping = {
                "ID1": "Drug_ID",
                "ID2": "Cell Line_ID",
                "X1": "Drug",
                "X2": "Cell Line"
            }

            self.benchmark_df = self.benchmark_df.rename(columns=column_mapping)
            print("Preprocessing completed successfully.")
            return self.benchmark_df

        except Exception as e:
            print(f"Error in preprocessing: {e}")
            return None

    def compare_dataframes(self):
        """
        Compares the benchmark dataset with the actual dataset
        """
        try:
            if self.gdsc_df is None or self.benchmark_df is None:
                raise ValueError("DataFrames are not loaded.")

            benchmark_df_renamed = self.preprocess_data()
            if benchmark_df_renamed is None:
                raise ValueError("Failed to preprocess the benchmark dataset.")

            benchmark_df_reordered = benchmark_df_renamed[self.gdsc_df.columns]
            
            print("Comparing DataFrames...")
            are_identical = self.gdsc_df.equals(benchmark_df_reordered)
            result = "Both DataFrames are the same." if are_identical else "Both DataFrames are different."
            
            return result
             
        except KeyError as ke:
            print(f"KeyError: {ke}. Ensure column names match between the datasets.")
            return None
            
        except Exception as e:
            print(f"Error comparing DataFrames: {e}")
            return None