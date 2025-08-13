import os
import zipfile

# Caminho da pasta com os arquivos ZIP
pasta_zip = r'C:\Users\Angelo\Desktop\MBA\ciencia_dados_tcc\downloads_ans'  # <--- altere esse caminho
pasta_saida = r'D:\base_ans'

# Cria a pasta "dezipados" se ela não existir
os.makedirs(pasta_saida, exist_ok=True)

# Itera por todos os arquivos na pasta
for nome_arquivo in os.listdir(pasta_zip):
    if nome_arquivo.lower().endswith('.zip'):
        caminho_zip = os.path.join(pasta_zip, nome_arquivo)
        try:
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(pasta_saida)
                print(f'Extraído: {nome_arquivo}')
        except zipfile.BadZipFile:
            print(f'Erro ao abrir: {nome_arquivo} (arquivo corrompido?)')
