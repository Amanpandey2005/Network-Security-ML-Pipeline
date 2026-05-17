import pandas as pd
import os

# Load main dataset
df = pd.read_csv("data/raw/network.csv")

# Remove label column
if "Label" in df.columns:
    df = df.drop("Label", axis=1)

# Take only first 100 rows
small_df = df.head(300)

# Create test folder
os.makedirs("data/test", exist_ok=True)

# Save test file
small_df.to_csv("data/test/test.csv", index=False)

print("Small test file created successfully")