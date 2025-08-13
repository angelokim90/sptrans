import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URL base do diretório
base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/informacoes_consolidadas_de_beneficiarios-024/"

# Pasta para salvar os arquivos
os.makedirs("downloads_ans", exist_ok=True)

# Loop de ano/mês de 202001 a 202504
for ano in range(2025, 2026):
    for mes in range(1, 13):
        pasta = f"{ano}{mes:02d}"
        if pasta > "202504":
            break  # Parar o loop após o mês final
        url_completa = urljoin(base_url, pasta + "/")
        print(f"\n📂 Acessando: {url_completa}")

        try:
            resposta = requests.get(url_completa, timeout=10)
            if resposta.status_code != 200:
                print(f"❌ Pasta não encontrada: {pasta}")
                continue

            soup = BeautifulSoup(resposta.text, "html.parser")
            links = soup.find_all("a")

            for link in links:
                href = link.get("href")
                if href and href.endswith(".zip"):
                    url_arquivo = urljoin(url_completa, href)
                    caminho_arquivo = os.path.join("downloads_ans", href)

                    # Evita baixar novamente
                    if os.path.exists(caminho_arquivo):
                        print(f"⏩ Já existe: {href}")
                        continue

                    print(f"⬇️  Baixando: {href}")
                    resp_arquivo = requests.get(url_arquivo)
                    with open(caminho_arquivo, "wb") as f:
                        f.write(resp_arquivo.content)
                    print(f"✔️ Salvo em: {caminho_arquivo}")
        except Exception as e:
            print(f"⚠️ Erro ao acessar {url_completa}: {e}")
