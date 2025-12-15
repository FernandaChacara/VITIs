USE vitis_project;

LOAD DATA INFILE 'K:/Fernanda/VITIs/processed_data/ndvi_alentejo_2023.csv'
INTO TABLE vegetation_index
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
  date,
  ndvi_mean
)
SET
  parcel_id = 1,
  source_id = 2;
