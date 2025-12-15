-- Create database
CREATE DATABASE IF NOT EXISTS vitis_project;
USE vitis_project;

-- =========================
-- User
-- =========================
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150)
);

-- =========================
-- Parcel
-- =========================
CREATE TABLE parcel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100),
    region VARCHAR(100),
    latitude DECIMAL(6,3),
    longitude DECIMAL(6,3),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- =========================
-- Data source
-- =========================
CREATE TABLE data_source (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    provider VARCHAR(100),
    licence VARCHAR(200)
);

-- =========================
-- Weather observation
-- =========================
CREATE TABLE weather_observation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    source_id INT NOT NULL,
    observation_time DATETIME NOT NULL,

    air_temperature_c FLOAT,
    dewpoint_temperature_c FLOAT,
    relative_humidity_pct FLOAT,

    precipitation_m FLOAT,
    solar_radiation_jm2 DOUBLE,

    wind_u_10m FLOAT,
    wind_v_10m FLOAT,

    evaporation_m FLOAT,

    FOREIGN KEY (parcel_id) REFERENCES parcel(id),
    FOREIGN KEY (source_id) REFERENCES data_source(id)
);

-- =========================
-- Vegetation index
-- =========================
CREATE TABLE vegetation_index (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    source_id INT NOT NULL,
    observation_time DATETIME NOT NULL,
    ndvi_mean FLOAT,
    FOREIGN KEY (parcel_id) REFERENCES parcel(id),
    FOREIGN KEY (source_id) REFERENCES data_source(id)
);

-- =========================
-- Analysis result
-- =========================
CREATE TABLE analysis_result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    observation_time DATETIME NOT NULL,
    vigor_class VARCHAR(50),
    stress_flag BOOLEAN,
    notes TEXT,
    FOREIGN KEY (parcel_id) REFERENCES parcel(id)
);
