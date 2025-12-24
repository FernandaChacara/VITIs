import pandas as pd

df = pd.read_csv("../processed_data/ndvi_alentejo_2023.csv")
parcels = pd.read_csv("../original_data/parcel.csv")
sources = pd.read_csv("../original_data/data_source.csv")

df.insert(0, "id", range(1, len(df) + 1))

parcel_ids = parcels["id"].tolist()
df["parcel_id"] = (parcel_ids * ((len(df) // len(parcel_ids)) + 1))[:len(df)]

copernicus_source_id = sources.loc[sources["name"].str.contains("Copernicus", case=False), "id"].values[0]
df["source_id"] = copernicus_source_id

df["observation_date"] = pd.to_datetime(df["date"]).dt.date

df = df.drop(columns=["date"])  # APENAS UMA VEZ

df.to_csv("../processed_data/ndvi_alentejo_2023_structured.csv", index=False)