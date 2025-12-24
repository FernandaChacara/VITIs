/* =========================================================
   Data Use Queries
   Vineyard vegetation, climate and irrigation analysis
   ========================================================= */

USE vitis_project;

/* =========================================================
   Q1: How does vegetation vigor evolve over time at parcel level?
   ========================================================= */

SELECT
    parcel_id,
    observation_date,
    ndvi_mean
FROM vegetation_index
ORDER BY parcel_id, observation_date;


/* =========================================================
   Q2: Are there differences in average vegetation vigor
       between parcels?
   ========================================================= */

SELECT
    parcel_id,
    AVG(ndvi_mean) AS avg_ndvi,
    MIN(ndvi_mean) AS min_ndvi,
    MAX(ndvi_mean) AS max_ndvi,
    COUNT(*) AS ndvi_observations
FROM vegetation_index
GROUP BY parcel_id
ORDER BY avg_ndvi DESC;


/* =========================================================
   Q3: What climatic conditions are associated with periods
       of low vegetation vigor?
   ========================================================= */

SELECT
    v.parcel_id,
    v.observation_date,
    v.ndvi_mean,
    w.air_temperature_c,
    w.precipitation_m,
    w.evaporation_m
FROM vegetation_index v
JOIN weather_observation w
    ON v.parcel_id = w.parcel_id
   AND DATE(w.observation_time) = v.observation_date
WHERE v.ndvi_mean < 0.4
ORDER BY v.parcel_id, v.observation_date;


/* =========================================================
   Q4: How frequent are irrigation events per parcel
       throughout the growing season?
   ========================================================= */

SELECT
    parcel_id,
    COUNT(*) AS irrigation_events,
    SUM(volume_liters) AS total_irrigation_volume,
    AVG(volume_liters) AS avg_irrigation_volume
FROM irrigation_log
GROUP BY parcel_id
ORDER BY irrigation_events DESC;


/* =========================================================
   Q5: Do parcels with more frequent irrigation show
       different vegetation vigor patterns?
   ========================================================= */

SELECT
    v.parcel_id,
    COUNT(DISTINCT i.id) AS irrigation_events,
    AVG(v.ndvi_mean) AS avg_ndvi
FROM vegetation_index v
LEFT JOIN irrigation_log i
    ON v.parcel_id = i.parcel_id
GROUP BY v.parcel_id
ORDER BY irrigation_events DESC;


/* =========================================================
   Q6: Monthly aggregation of NDVI and irrigation activity
       to support seasonal analysis
   ========================================================= */

SELECT
    v.parcel_id,
    YEAR(v.observation_date) AS year,
    MONTH(v.observation_date) AS month,
    AVG(v.ndvi_mean) AS monthly_avg_ndvi,
    COUNT(i.id) AS monthly_irrigation_events
FROM vegetation_index v
LEFT JOIN irrigation_log i
    ON v.parcel_id = i.parcel_id
   AND YEAR(i.irrigation_time) = YEAR(v.observation_date)
   AND MONTH(i.irrigation_time) = MONTH(v.observation_date)
GROUP BY v.parcel_id, year, month
ORDER BY v.parcel_id, year, month;

/* =========================================================
   Q7: Are there parcels associated with low regional NDVI
       values and no recent irrigation activity?
   ========================================================= */

SELECT
    v.parcel_id,
    v.observation_date,
    v.ndvi_mean,
    MAX(i.irrigation_time) AS last_irrigation
FROM vegetation_index v
LEFT JOIN irrigation_log i
    ON v.parcel_id = i.parcel_id
   AND i.irrigation_time <= v.observation_date
WHERE v.ndvi_mean < 0.4
GROUP BY v.parcel_id, v.observation_date, v.ndvi_mean
HAVING last_irrigation IS NULL
   OR DATEDIFF(v.observation_date, last_irrigation) > 14
ORDER BY v.parcel_id, v.observation_date;

/* =========================================================
   Q8: Which parcels are associated with higher temporal
       variability of regional NDVI values?
   ========================================================= */

SELECT
    parcel_id,
    COUNT(*) AS ndvi_observations,
    AVG(ndvi_mean) AS avg_ndvi,
    STDDEV(ndvi_mean) AS ndvi_variability
FROM vegetation_index
GROUP BY parcel_id
ORDER BY ndvi_variability DESC;

/* =========================================================
   Q9: What are the average climatic conditions during
       periods when NDVI observations are available?
   ========================================================= */

SELECT
    v.parcel_id,
    AVG(w.air_temperature_c) AS avg_temperature,
    AVG(w.precipitation_m) AS avg_precipitation,
    AVG(w.evaporation_m) AS avg_evaporation
FROM vegetation_index v
JOIN weather_observation w
    ON v.parcel_id = w.parcel_id
   AND DATE(w.observation_time) = v.observation_date
GROUP BY v.parcel_id
ORDER BY v.parcel_id;


/* =========================================================
   End of data use queries
   ========================================================= */

