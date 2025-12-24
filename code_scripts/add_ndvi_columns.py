import pandas as pd

# Load the NDVI CSV from processed data (original was too heavy to version)
df = pd.read_csv("../processed_data/ndvi_alentejo_2023.csv")

# Create a sequential unique ID column for PRIMARY KEY
df.insert(0, "id", range(1, len(df) + 1))

# Add parcel_id column (temporary placeholder, ensures import works)
df["parcel_id"] = 1

# Add source_id column (Copernicus NDVI has id=2 in the DB)
df["source_id"] = 2

# Convert date column into MariaDB DATETIME format
df["observation_time"] = pd.to_datetime(df["date"])

# Remove old date column to match DB field names
df = df.drop(columns=["date"])

# Save the new file ready for database import
df.to_csv("../processed_data/ndvi_ready.csv", index=False)
