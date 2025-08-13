from pyspark.sql import SparkSession
import time
import os

caminho =r'D:/base_ans_parquet/'

spark = SparkSession.builder.appName("LeituraParquet").getOrCreate()

arquivos_parquet = [
    os.path.join(caminho, f)
    for f in os.listdir(caminho)
    if f.endswith(".parquet")
]
inicio = time.time()

df = spark.read.parquet(*arquivos_parquet)
total_registros = df.count()  # Força leitura e conta registros
fim = time.time()

print(f"Total de registros: {total_registros}")
print(f"Tempo de leitura: {fim - inicio:.2f} segundos")