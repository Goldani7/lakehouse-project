# 02_silver_transformation.py
# Camada Silver: limpeza, tipagem correta e enforcement de schema

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType, DateType, BooleanType

spark = SparkSession.builder.appName("silver_transformation").getOrCreate()

BRONZE_PATH = "data/bronze/repos/"
SILVER_PATH = "data/silver/repos/"

df = spark.read.format("delta").load(BRONZE_PATH)

df_clean = (
    df
    # remove duplicados exatos e repositórios sem nome
    .dropDuplicates(["full_name"])
    .filter(F.col("full_name").isNotNull())
    # tipagem numérica
    .withColumn("stars", F.col("stars").cast(IntegerType()))
    .withColumn("forks", F.col("forks").cast(IntegerType()))
    .withColumn("open_issues", F.col("open_issues").cast(IntegerType()))
    .withColumn("size_kb", F.col("size_kb").cast(DoubleType()))
    .withColumn("repo_age_days", F.col("repo_age_days").cast(IntegerType()))
    .withColumn("days_since_last_push", F.col("days_since_last_push").cast(IntegerType()))
    .withColumn("github_health_pct", F.col("github_health_pct").cast(DoubleType()))
    .withColumn("releases_count", F.col("releases_count").cast(IntegerType()))
    .withColumn("release_cadence_days", F.col("release_cadence_days").cast(DoubleType()))
    # tipagem de datas
    .withColumn("created_at", F.to_timestamp("created_at"))
    .withColumn("updated_at", F.to_timestamp("updated_at"))
    .withColumn("pushed_at", F.to_timestamp("pushed_at"))
    .withColumn("latest_release_date", F.to_timestamp("latest_release_date"))
    # tipagem booleana
    .withColumn("archived", F.col("archived").cast(BooleanType()))
    .withColumn("has_readme_file", F.col("has_readme_file").cast(BooleanType()))
    .withColumn("has_contributing_file", F.col("has_contributing_file").cast(BooleanType()))
    .withColumn("has_code_of_conduct", F.col("has_code_of_conduct").cast(BooleanType()))
    .withColumn("has_issue_template", F.col("has_issue_template").cast(BooleanType()))
    .withColumn("has_license_file", F.col("has_license_file").cast(BooleanType()))
    # tratamento de nulos em texto
    .fillna({
        "license": "Unknown",
        "language": "Unknown",
        "ai_category": "Uncategorized",
        "framework_stack": "None",
        "maintenance_status": "Unknown",
    })
    # transforma topics/framework_stack (separados por ";") em arrays
    .withColumn("topics_list", F.split(F.col("topics"), ";"))
    .withColumn("framework_list", F.split(F.col("framework_stack"), ";"))
)

df_clean.write.format("delta").mode("overwrite").save(SILVER_PATH)

print(f"Transformação Silver concluída: {df_clean.count()} registros")
