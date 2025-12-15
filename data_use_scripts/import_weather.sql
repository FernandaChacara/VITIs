USE vitis_project;

LOAD DATA INFILE '/ABSOLUTE/PATH/TO/processed_data/era5_alentejo_clean.csv'
INTO TABLE weather_observation
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
  observation_time,
  air_temperature_c,
  dewpoint_temperature_c,
  relative_humidity_pct,
  precipitation_m,
  solar_radiation_jm2,
  wind_u_10m,
  wind_v_10m,
  evaporation_m
)
SET
  parcel_id = 1,
  source_id = 1;
