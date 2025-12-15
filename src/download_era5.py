import cdsapi

c = cdsapi.Client()

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
        'month': [f'{m:02d}' for m in range(1, 13)],
        'day': [f'{d:02d}' for d in range(1, 32)],
        'time': '12:00',
        'area': [39, -7, 38, -8],  # Alentejo (recorte pequeno)
    },
    '../original_data/era5_alentejo.nc'
)

print("ERA5 download for full year completed.")

