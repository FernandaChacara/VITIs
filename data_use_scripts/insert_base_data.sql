USE vitis_project;

-- User
INSERT INTO user (name, email)
VALUES ('Demo User', 'demo@vitis.app');

-- Parcel
INSERT INTO parcel (user_id, name, region, latitude, longitude)
VALUES (1, 'Alentejo Vineyard', 'Alentejo', 38.5, -7.9);

-- Data sources
INSERT INTO data_source (name, provider, licence)
VALUES
('ERA5', 'Copernicus Climate Change Service', 'Copernicus Licence'),
('Sentinel-2 NDVI', 'Copernicus', 'Copernicus Licence');
