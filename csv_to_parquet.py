import os
import pandas as pd

# Caminho da pasta com os CSVs
pasta_csv = r'D:\base_ans'  # <--- altere esse caminho
pasta_parquet =  r'D:\base_ans_parquet'
os.makedirs(pasta_parquet, exist_ok=True)

# Loop por todos os arquivos CSV
for arquivo in os.listdir(pasta_csv):
    if arquivo.lower().endswith('.csv'):
        caminho_csv = os.path.join(pasta_csv, arquivo)
        nome_base = os.path.splitext(arquivo)[0]
        caminho_parquet = os.path.join(pasta_parquet, f'{nome_base}.parquet')

        try:
            print(f'Convertendo: {arquivo}')
            df = pd.read_csv(caminho_csv,delimiter=';', quotechar='"')
            df.to_parquet(caminho_parquet, index=False)  # usa pyarrow ou fastparquet
        except Exception as e:
            print(f'Erro ao converter {arquivo}: {e}')
