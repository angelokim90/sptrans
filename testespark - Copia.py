from pyspark.sql import SparkSession

# Criar a sessão Spark
spark = SparkSession.builder \
    .appName("Leitura Parquet") \
    .getOrCreate()

# Ler o arquivo Parquet
df = spark.read.parquet(r"D:\base_ans_parquet\pda-024-icb-AC-2020_01.parquet")

# Mostrar os primeiros registros
df.show()
