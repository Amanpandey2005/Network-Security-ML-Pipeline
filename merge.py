import pandas as pd
import glob
import os

# Path of CSV files
path = "data/raw/"

# Get all CSV files
all_files = glob.glob(os.path.join(path, "*.csv"))

print("Total files found:", len(all_files))

df_list = []

# Read all CSVs
for file in all_files:

    print("Reading:", file)

    try:

        df = pd.read_csv(file, low_memory=False)

        df_list.append(df)

        print("Loaded:", df.shape)

    except Exception as e:

        print("Error in", file)

        print(e)

# Merge all files
merged_df = pd.concat(
    df_list,
    ignore_index=True
)

# Save merged dataset
output_path = "data/raw/network.csv"

merged_df.to_csv(
    output_path,
    index=False
)

print("\nMerged Successfully")

print("Final Shape:", merged_df.shape)

# Show attack distribution
print("\nLabels Distribution:\n")

print(merged_df["Label"].value_counts())