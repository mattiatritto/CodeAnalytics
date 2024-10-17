import pandas as pd
from scipy.io import arff
import os

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# List of dataset files (relative paths)
file_paths = [
    os.path.join(script_dir, "..", "datasets", "1-china.arff"),
    os.path.join(script_dir, "..", "datasets", "3-kemerer.arff"),
    os.path.join(script_dir, "..", "datasets", "4-kitchenham.arff"),
]

# List of the different column names to select for each dataset
columns_to_select = [
    ["AFP", "Duration", "Effort"],  # china dataset
    ["AdjFP", "Duration", "EffortMM"],  # kemerer dataset
    [
        "Adjusted.function.points",
        "Actual.duration",
        "Actual.effort",
    ],  # kitchenham dataset
]

# New column names that will be the same for all datasets after selection
new_column_names = ["AFP", "Duration", "Effort"]

# List to store the DataFrames
dfs = []

# Loop over each dataset file and its corresponding columns to select
for file_path, col_names in zip(file_paths, columns_to_select):
    # Load the .arff file
    data, meta = arff.loadarff(file_path)

    # Convert it to a DataFrame
    df = pd.DataFrame(data)

    # Check for missing values in the selected columns
    missing_values_selected = df[col_names].isnull().sum()

    print(f"\nProcessing file: {file_path}")
    print("Are there any missing values?")
    print(missing_values_selected)

    # Select the specific columns for the current dataset
    df_selected = df[col_names]

    # Rename columns to the unified names ('AFP', 'Duration', 'Effort')
    df_selected.columns = new_column_names

    # Add the DataFrame to the list
    dfs.append(df_selected)

    # Print descriptive statistics for the current DataFrame
    print("\nDescriptive statistics:")
    print(df_selected.describe())

# Concatenate all DataFrames into a single DataFrame
final_df = pd.concat(dfs, ignore_index=True)

# Create the path for the output CSV
output_path = os.path.join(script_dir, "..", "datasets", "5-unified_dataset.csv")

# Ensure the directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the final DataFrame as a CSV file
final_df.to_csv(output_path, index=False)

print(f"\nFinal dataset saved to {output_path}")
