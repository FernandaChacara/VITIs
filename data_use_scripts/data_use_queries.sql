USE vitis_project;

-- 1) Daily climate summary (temperature, humidity, precipitation, radiation)
SELECT
  observation_time,
  air_temperature_c,
  relative_humidity_pct,
  precipitation_m,
  solar_radiation_jm2
FROM weather_observation
ORDER BY observation_time;

-- 2) Monthly climate averages and totals
SELECT
  MONTH(observation_time) AS month,
  AVG(air_temperature_c) AS avg_temperature_c,
  AVG(relative_humidity_pct) AS avg_relative_humidity_pct,
  SUM(precipitation_m) AS total_precipitation_m
FROM weather_observation
GROUP BY MONTH(observation_time)
ORDER BY month;

-- 3) Thermal stress days (air temperature above 30 °C)
SELECT
  observation_time,
  air_temperature_c
FROM weather_observation
WHERE air_temperature_c > 30
ORDER BY observation_time;

-- 4) Dry days (no precipitation)
SELECT
  observation_time
FROM weather_observation
WHERE precipitation_m = 0;
