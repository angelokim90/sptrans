from minio import Minio
from minio.commonconfig import CopySource
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, current_timestamp, from_utc_timestamp
import datetime
import pytz
import re

# === Spark Session ===
spark = (
    SparkSession
    .builder
    .appName('pipeline_sptrans')
    .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension')
    .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog')
    .config("spark.hadoop.fs.s3a.access.key", "datalake")
    .config("spark.hadoop.fs.s3a.secret.key", "datalake")
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .getOrCreate()
)

# === MinIO Client ===
client = Minio(
    "minio:9000",
    access_key="datalake",
    secret_key="datalake",
    secure=False
)

# === Paths e datas ===
hoje = datetime.datetime.today()
d = hoje.astimezone(pytz.timezone('America/Sao_Paulo'))
data_str = d.strftime('%Y-%m-%d')

bucket_raw = "raw"
origem_raw = f"api/{data_str}/"
bucket_trusted = "trusted"
path_trusted = "s3a://trusted/"

# === PostgreSQL ===
postgres_url = "jdbc:postgresql://db:5432/db?bronze_sptrans"
properties = {
    "user": "admin",
    "password": "admin",
    "driver": "org.postgresql.Driver"
}

# === Listar arquivos raw do dia ===

objetos = list(client.list_objects(bucket_raw, prefix=origem_raw, recursive=False))

if not objetos:
    print("Nenhum arquivo encontrado na pasta de origem.")
else:
    print(f"Arquivos encontrados em {bucket_raw}/{origem_raw}:")
    for obj in objetos:
        print(f"- Nome: {obj.object_name}, Tamanho: {obj.size} bytes")

if not objetos:
    print("Nenhum arquivo encontrado na pasta de origem.")
else:
    for obj in objetos:
        if obj.size > 0 and re.match(r'^[a-zA-Z0-9]', obj.object_name.split('/')[-1]):
            #print("passou do if")
            path_file = f"s3a://{bucket_raw}/{obj.object_name}"
            print(f"Lendo arquivo: {path_file}")

            # === Leitura e transformação ===
            df_raw = spark.read.option("multiline", "true").json(path_file)

            df_exploded = df_raw.select(
                col("hr"),
                explode(col("l")).alias("item")
            )

            df_final = df_exploded.select(
                col("hr"),
                col("item.c").alias("c"),
                col("item.cl").alias("cl"),
                col("item.sl").alias("sl"),
                col("item.lt0").alias("lt0"),
                col("item.lt1").alias("lt1"),
                col("item.qv").alias("qv"),
                explode(col("item.vs")).alias("vs_item")
            ).select(
                col("hr"),
                col("c"),
                col("cl"),
                col("sl"),
                col("lt0"),
                col("lt1"),
                col("qv"),
                col("vs_item.p").alias("p"),
                col("vs_item.a").alias("a"),
                col("vs_item.ta").alias("ta"),
                col("vs_item.py").alias("py"),
                col("vs_item.px").alias("px"),
                col("vs_item.sv").alias("sv"),
                col("vs_item.is").alias("vs_is")
            ).withColumn("dt_processamento", from_utc_timestamp(current_timestamp(), "America/Sao_Paulo"))

            # === Gravação no Delta (trusted) ===
            df_final.write.format("delta").option("mergeSchema", "true").mode("append").save(path_trusted)
            df_parquet_trusted = spark.read.parquet(path_trusted)
            try:    
                df_parquet_trusted.write.jdbc(url=postgres_url, table="bronze_sptrans.posicao", mode="append", properties=properties)
                print("Conexão bem-sucedida!")
            except Exception as e:
                print(f"Erro ao conectar ao PostgreSQL: {e}")
            

            # === Inserir log no PostgreSQL ===
            conn = spark._sc._gateway.jvm.java.sql.DriverManager.getConnection(
                postgres_url, properties["user"], properties["password"]
            )
            stmt = conn.createStatement()
            insert_log = f"""
                INSERT INTO db.monitoramento_log.processamento_arquivo(nm_arquivo, dt_processamento, nr_tamanho_byte)
                VALUES('{obj.object_name}', CURRENT_TIMESTAMP, {obj.size})
            """
            stmt.execute(insert_log)
            df_parquet_trusted.write.jdbc(url=postgres_url, table="bronze_sptrans.posicao", mode="append", properties=properties)
            stmt.close()
            conn.close()

            # === Move arquivo para processed no raw ===
            destino_arquivo = obj.object_name.replace(origem_raw, origem_raw + "processed/", 1)
            source = CopySource(bucket_raw, obj.object_name)
            client.copy_object(bucket_raw, destino_arquivo, source)
            client.remove_object(bucket_raw, obj.object_name)

            print(f"Arquivo processado e movido: {obj.object_name}")

# === Finaliza Spark ===
spark.stop()
