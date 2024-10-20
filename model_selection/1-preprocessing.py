import os
import numpy as np
import pandas as pd
from scipy.io import arff



print("[1]: Loading CHINA dataset...")
dataset_file_path = os.path.abspath("datasets/1-china.arff")
data, meta = arff.loadarff(dataset_file_path)
dataset = pd.DataFrame(data)



print("[2]: Taking only features of interest...")
features = ["AFP", "Effort", "Input", "Output", "Enquiry", "File", "Interface", "Duration"]
dataset = dataset[features].copy()



print("[3]: Creating new rows by adding some small gaussian random noise...")
new_rows = []
for index, row in dataset.iterrows():
    np.random.seed(index)
    noise = np.random.normal(loc=0, scale=0.15, size=len(features))
    noisy_row = (row + noise).round().astype(int)
    new_rows.append(noisy_row)



print("[4]: Append new rows with the previous ones...")
dataset_augmented = pd.DataFrame(new_rows, columns=features)
final_dataset = pd.concat([dataset, dataset_augmented], axis=0).reset_index(drop=True)



print("[5]: Saving the new dataset as 1-china-augmented.csv...")
output_file_path = "datasets/1-china-augmented.csv"
final_dataset.to_csv(output_file_path, index=False)