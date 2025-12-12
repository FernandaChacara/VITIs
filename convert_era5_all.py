import xarray as xr
import pandas as pd
import os

# Pastas
input_folder = "original_data"
output_folder = "processed_data"

# Criar pasta de saída se não existir
os.makedirs(output_folder, exist_ok=True)

# Listar todos os .nc
files = [f for f in os.listdir(input_folder) if f.endswith(".nc")]

print(f"Encontrados {len(files)} arquivos NetCDF para converter.\n")

for f in files:
    input_path = os.path.join(input_folder, f)
    
    print(f"Convertendo: {f}")

    # Abrir dataset NetCDF
    ds = xr.open_dataset(input_path, engine="netcdf4")
    
    # Converter para DataFrame
    df = ds.to_dataframe().reset_index()
    
    # Nome do CSV de saída
    output_path = os.path.join(output_folder, f.replace(".nc", ".csv"))
    
    # Salvar CSV
    df.to_csv(output_path, index=False)
    
    print(f" → Salvo como: {output_path}\n")

print("Conversão concluída para todos os arquivos ERA5!")
