import xarray as xr
import pandas as pd
import os
import zipfile
import shutil

input_folder = "original_data"
output_folder = "processed_data"

os.makedirs(output_folder, exist_ok=True)

# Criar pasta temporária GLOBAL fora de original_data
temp_dir = "_tmp_nc_extract"
os.makedirs(temp_dir, exist_ok=True)

files = [f for f in os.listdir(input_folder) if f.endswith(".nc")]

print(f"Procurando arquivos para converter...\nEncontrados {len(files)} arquivos.\n")

for f in files:
    print(f"Processando: {f}")

    input_path = os.path.join(input_folder, f)

    # Limpar pasta temporária ANTES de extrair
    for item in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, item))

    # Abrir o .nc que é ZIP
    try:
        with zipfile.ZipFile(input_path, "r") as z:
            z.extractall(temp_dir)
            print(f" - Extraído para: {temp_dir}")
    except:
        print("ERRO: arquivo não parece ZIP!")
        continue

    # Achar o .nc verdadeiro dentro da pasta temporária
    nc_inside = [x for x in os.listdir(temp_dir) if x.endswith(".nc")]
    if not nc_inside:
        print("ERRO: Nenhum arquivo .nc dentro do ZIP!")
        continue

    real_nc_path = os.path.join(temp_dir, nc_inside[0])
    print(f" - Abrindo NetCDF real: {nc_inside[0]}")

    # Abrir o NetCDF com engine explícito
    ds = xr.open_dataset(real_nc_path, engine="netcdf4")

    # Converter para DataFrame
    df = ds.to_dataframe().reset_index()

    # Criar nome final do CSV
    csv_name = f.replace(".nc", ".csv")
    csv_path = os.path.join(output_folder, csv_name)

    # Salvar
    df.to_csv(csv_path, index=False)
    print(f" ✔ CSV salvo em: {csv_path}\n")

print("Conversão concluída!")

