# 01_bronze_ingestion.py
# Camada Bronze: ingestão de dados brutos, sem transformação (schema-on-read)
#
# Dataset: AI Engineering Ecosystem Intelligence
# ~30 mil repositórios do GitHub sobre engenharia de IA (frameworks, agentes, RAG, etc.)

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("bronze_ingestion").getOrCreate()

RAW_PATH = "data/raw/ai_engineering_ecosystem_intelligence.csv"
BRONZE_PATH = "data/bronze/repos/"

df = spark.read.option("header", True).option("multiLine", True).option("escape", '"').csv(RAW_PATH)

df.write.format("delta").mode("overwrite").save(BRONZE_PATH)

print(f"Ingestão Bronze concluída: {df.count()} registros, {len(df.columns)} colunas")
