import cdsapi

# Initialize CDS API client
c = cdsapi.Client()

# Download ERA5 data for Alentejo (April 2023)
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            '2m_temperature',
            '2m_dewpoint_temperature',
            'total_precipitation',
            'surface_solar_radiation_downwards',
            '10m_u_component_of_wind',
            '10m_v_component_of_wind',
            'evaporation',
        ],
        'year': '2023',
        'month': '04',
        'day': [f'{d:02d}' for d in range(1, 31)],
        'time': '12:00',
        'area': [39, -7, 38, -8],   # North, West, South, East (small box around Alentejo)
    },
    '../original_data/era5_alentejo.nc'
)

print("Download complete: era5_alentejo.nc saved to original_data/")
