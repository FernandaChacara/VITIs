import xarray as xr
import pandas as pd
import os
import zipfile
import shutil

input_folder = "original_data"
output_folder = "processed_data"
temp_dir = "_tmp_nc_extract"

os.makedirs(output_folder, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

files = [f for f in os.listdir(input_folder) if f.endswith(".nc")]

print(f"Procurando arquivos para converter...\nEncontrados {len(files)} arquivos.\n")

for f in files:
    print(f"Processando: {f}")

    input_path = os.path.join(input_folder, f)

    # 1) LIMPAR PASTA TEMPORÁRIA SEM REMOVER ARQUIVOS EM USO
    for item in os.listdir(temp_dir):
        try:
            os.remove(os.path.join(temp_dir, item))
        except PermissionError:
            pass

    # 2) EXTRair ZIP (.nc falso)
    with zipfile.ZipFile(input_path, "r") as z:
        z.extractall(temp_dir)
        print(" - Extraído para pasta temporária.")

    # 3) Identificar o arquivo .nc REAL
    extracted = [x for x in os.listdir(temp_dir) if x.endswith(".nc")]
    if not extracted:
        print("ERRO: nenhum NetCDF real encontrado.")
        continue

    real_nc = os.path.join(temp_dir, extracted[0])
    print(f" - NetCDF real: {real_nc}")

    # 4) Abrir dataset
    ds = xr.open_dataset(real_nc, engine="netcdf4")

    # 5) Converter → DataFrame
    df = ds.to_dataframe().reset_index()

    # 6) Nome do CSV
    csv_path = os.path.join(output_folder, f.replace(".nc", ".csv"))

    # 7) Salvar CSV
    df.to_csv(csv_path, index=False)
    print(f" ✔ CSV salvo em: {csv_path}")

    # 8) FECHAR O DATASET (resolve o erro do Windows!)
    ds.close()

    # 9) AGORA PODE remover o .nc
    try:
        os.remove(real_nc)
    except PermissionError:
        print("Aviso: arquivo ainda preso. Ignorando para continuar…")

    print("")

print("Conversão concluída!")


