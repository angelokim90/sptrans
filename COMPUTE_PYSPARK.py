from pyspark.sql import SparkSession
import os

caminho_base = r"D:\base_ans_parquet\pda-024-icb-AC-2020_01.parquet"

# Verificação prévia: o arquivo existe?
# 1. Criar a sessão do Spark
print("1. Iniciando sessão Spark...")
spark = SparkSession.builder \
.appName("BeneficiariosANS") \
    .master("local[*]") \
    .config("spark.hadoop.io.native.lib.available", "true") \
    .config("spark.hadoop.hadoop.security.access.control", "true") \
    .getOrCreate()


print("→ Sessão Spark criada com sucesso.")

# 2. Leitura do arquivo parquet
print("2. Iniciando leitura do arquivo parquet...")
try:
    df = spark.read.parquet(caminho_base)
    print("→ Leitura concluída.")
except Exception as e:
    print("⚠️ Erro ao ler o arquivo:", e)
    spark.stop()
    raise SystemExit()

# 3. Exibir estrutura e primeiras linhas
print("3. Estrutura do DataFrame:")
df.printSchema()

print("4. Primeiras 5 linhas do DataFrame:")
df.show(5)

# 4. Operações: exemplo de agrupamento (descomente se quiser testar)
# print("5. Agrupamento por CD_CONTRATO:")
# df.groupBy("CD_CONTRATO").count().show()

# 5. Gravar resultado como Parquet (opcional)
# print("6. Gravando resultado em parquet...")
# df.write.mode("overwrite").parquet("saida/beneficiarios.parquet")
# print("→ Arquivo gravado com sucesso.")
