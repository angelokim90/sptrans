import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URL base
base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/informacoes_consolidadas_de_beneficiarios-024/"
mesano = "202505/"
base_url = base_url + mesano

# Pasta local para salvar
os.makedirs("downloads_ans", exist_ok=True)

# Requisição e parsing do HTML da página
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Encontrar todos os links para arquivos ZIP
links = soup.find_all("a")

for link in links:
    href = link.get("href")
    if href.endswith(".zip"):
        file_url = urljoin(base_url, href)
        print(f"Baixando: {file_url}")

        response_file = requests.get(file_url)
        caminho_arquivo = os.path.join("downloads_ans", href)

        with open(caminho_arquivo, "wb") as f:
            f.write(response_file.content)

        print(f"✔️ Arquivo salvo: {caminho_arquivo}")
