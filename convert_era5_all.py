import xarray as xr
import pandas as pd
import os
import zipfile

input_folder = "original_data"
output_folder = "processed_data"

os.makedirs(output_folder, exist_ok=True)

def is_zip_disguised_as_nc(file_path):
    """Checa se o arquivo .nc é na verdade um ZIP."""
    with open(file_path, "rb") as f:
        signature = f.read(4)
    return signature == b"PK\x03\x04"  # assinatura ZIP

def extract_zip_nc(file_path, temp_dir):
    """Extrai o conteúdo do arquivo ZIP e retorna o caminho do .nc verdadeiro."""
    os.makedirs(temp_dir, exist_ok=True)
    with zipfile.ZipFile(file_path, "r") as z:
        z.extractall(temp_dir)
        # pegar o primeiro arquivo extraído
        for root, _, files in os.walk(temp_dir):
            for f in files:
                if f.endswith(".nc"):
                    return os.path.join(root, f)
    return None

print("Procurando arquivos para converter...")
files = sorted([f for f in os.listdir(input_folder) if f.endswith(".nc")])

print(f"Encontrados {len(files)} arquivos.")

for f in files:
    input_path = os.path.join(input_folder, f)
    print(f"\nProcessando: {f}")

    # 1. Checar se é um ZIP disfarçado
    if is_zip_disguised_as_nc(input_path):
        print(" → Arquivo é ZIP (travestido de .nc). Extraindo...")
        temp_dir = os.path.join(input_folder, "tmp_extract")

        real_nc_path = extract_zip_nc(input_path, temp_dir)

        if real_nc_path is None:
            print("ERRO: Nenhum .nc encontrado dentro do ZIP!")
            continue

        print(f" → Extraído: {real_nc_path}")
        open_path = real_nc_path

    else:
        open_path = input_path

    # 2. Abrir com xarray
    print(" → Abrindo dataset com xarray...")
    try:
        ds = xr.open_dataset(open_path)
    except Exception as e:
        print("ERRO ao abrir com xarray:", e)
        continue

    # 3. Converter para DataFrame
    print(" → Convertendo para DataFrame...")
    df = ds.to_dataframe().reset_index()

    # 4. Salvar CSV
    out_csv = os.path.join(output_folder, f.replace(".nc", ".csv"))
    df.to_csv(out_csv, index=False)

    print(f" ✔ CSV salvo em: {out_csv}")

print("\nConversão concluída!")

