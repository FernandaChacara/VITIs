/* =========================================================
   Database context
   ========================================================= */

USE vitis_project;


/* =========================================================
   Load USERS data
   ========================================================= */

LOAD DATA LOCAL INFILE 'C:/Users/islec/VITIs/original_data/user.csv'
INTO TABLE user
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, name, email, phone, affiliation);

/* Verification: number of users loaded */
SELECT COUNT(*) AS user_count FROM user;


/* =========================================================
   Load PARCELS data
   ========================================================= */

LOAD DATA LOCAL INFILE 'C:/Users/islec/VITIs/original_data/parcel.csv'
INTO TABLE parcel
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, user_id, name, region, latitude, longitude, area_ha);

/* Verification: number of parcels loaded */
SELECT COUNT(*) AS parcel_count FROM parcel;

/* Verification: each parcel must be associated with a user */
SELECT COUNT(*) AS parcels_without_user
FROM parcel
WHERE user_id NOT IN (SELECT id FROM user);


/* =========================================================
   Load DATA SOURCES
   ========================================================= */

LOAD DATA LOCAL INFILE 'C:/Users/islec/VITIs/original_data/data_source.csv'
INTO TABLE data_source
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, name, provider, licence);

/* Verification: number of data sources loaded */
SELECT COUNT(*) AS data_source_count FROM data_source;


/* =========================================================
   Load WEATHER OBSERVATIONS (ERA5)
   ========================================================= */

TRUNCATE TABLE weather_observation;

LOAD DATA LOCAL INFILE 'C:/Users/islec/VITIs/processed_data/era5_alentejo_structured.csv'
INTO TABLE weather_observation
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(parcel_id, source_id, observation_time,
 air_temperature_c, dewpoint_temperature_c, relative_humidity_pct,
 precipitation_m, solar_radiation_jm2,
 wind_u_10m, wind_v_10m, evaporation_m);

/* Verification: number of weather observations loaded */
SELECT COUNT(*) AS weather_observation_count FROM weather_observation;

/* Verification: weather observations must reference existing parcels */
SELECT COUNT(*) AS weather_without_parcel
FROM weather_observation
WHERE parcel_id NOT IN (SELECT id FROM parcel);


/* =========================================================
   Load VEGETATION INDEX (NDVI)
   ========================================================= */

TRUNCATE TABLE vegetation_index;

LOAD DATA LOCAL INFILE 'C:/Users/islec/VITIs/processed_data/ndvi_alentejo_2023_structured.csv'
INTO TABLE vegetation_index
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, ndvi_mean, parcel_id, source_id, observation_date);

/* Verification: number of NDVI records loaded */
SELECT COUNT(*) AS vegetation_index_count FROM vegetation_index;

/* Verification: NDVI records must reference existing parcels */
SELECT COUNT(*) AS ndvi_without_parcel
FROM vegetation_index
WHERE parcel_id NOT IN (SELECT id FROM parcel);


/* =========================================================
   Load IRRIGATION LOG (simulated management data)
   ========================================================= */

TRUNCATE TABLE irrigation_log;

LOAD DATA LOCAL INFILE 'C:/Users/islec/VITIs/original_data/irrigation_log.csv'
INTO TABLE irrigation_log
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(parcel_id, irrigation_time, volume_liters, method, notes);

/* Verification: number of irrigation events loaded */
SELECT COUNT(*) AS irrigation_event_count FROM irrigation_log;

/* Verification: number of parcels with irrigation records */
SELECT COUNT(DISTINCT parcel_id) AS irrigated_parcels
FROM irrigation_log;


/* =========================================================
   Final data review and sanity checks
   ========================================================= */

/* --- Overview: total records per table --- */

SELECT COUNT(*) AS user_count FROM user;
SELECT COUNT(*) AS parcel_count FROM parcel;
SELECT COUNT(*) AS data_source_count FROM data_source;
SELECT COUNT(*) AS weather_observation_count FROM weather_observation;
SELECT COUNT(*) AS vegetation_index_count FROM vegetation_index;
SELECT COUNT(*) AS irrigation_event_count FROM irrigation_log;


/* --- Sample records from each table --- */

SELECT * FROM user LIMIT 5;
SELECT * FROM parcel LIMIT 5;
SELECT * FROM data_source LIMIT 5;

SELECT
    parcel_id,
    observation_time,
    air_temperature_c,
    precipitation_m
FROM weather_observation
LIMIT 5;

SELECT
    parcel_id,
    observation_date,
    ndvi_mean
FROM vegetation_index
ORDER BY observation_date
LIMIT 5;

SELECT
    parcel_id,
    irrigation_time,
    volume_liters,
    method
FROM irrigation_log
ORDER BY irrigation_time
LIMIT 5;


/* --- Basic consistency checks --- */

/* Each parcel should have weather observations */
SELECT
    p.id AS parcel_id,
    COUNT(w.id) AS weather_records
FROM parcel p
LEFT JOIN weather_observation w ON p.id = w.parcel_id
GROUP BY p.id
ORDER BY p.id
LIMIT 10;

/* NDVI temporal coverage per parcel */
SELECT
    parcel_id,
    MIN(observation_date) AS first_ndvi_date,
    MAX(observation_date) AS last_ndvi_date,
    COUNT(*) AS ndvi_observations
FROM vegetation_index
GROUP BY parcel_id
ORDER BY parcel_id
LIMIT 10;

/* Irrigation frequency per parcel */
SELECT
    parcel_id,
    COUNT(*) AS irrigation_events
FROM irrigation_log
GROUP BY parcel_id
ORDER BY irrigation_events DESC
LIMIT 10;

SELECT * FROM user;
SELECT * FROM parcel;
SELECT * FROM data_source;
SELECT * FROM weather_observation LIMIT 50;
SELECT * FROM vegetation_index LIMIT 50;
SELECT * FROM irrigation_log LIMIT 50;

/* =========================================================
   End of script
   ========================================================= */
