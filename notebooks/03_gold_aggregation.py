# 03_gold_aggregation.py
# Camada Gold: métricas de negócio prontas para consumo (Power BI)
#
# Pergunta de negócio: quais frameworks/categorias de IA estão mais
# populares, mais saudáveis (manutenção) e mais ativos no GitHub?

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("gold_aggregation").getOrCreate()

SILVER_PATH = "data/silver/repos/"
GOLD_PATH = "data/gold/"

df = spark.read.format("delta").load(SILVER_PATH)

# 1) Panorama por categoria de IA (Agent/Orchestration, RAG, etc.)
gold_by_category = (
    df.groupBy("ai_category")
    .agg(
        F.count("*").alias("total_repos"),
        F.sum("stars").alias("total_stars"),
        F.avg("github_health_pct").alias("health_medio_pct"),
        F.avg("release_cadence_days").alias("cadencia_release_media_dias"),
    )
    .orderBy(F.desc("total_stars"))
)
gold_by_category.write.format("delta").mode("overwrite").save(GOLD_PATH + "por_categoria/")

# 2) Panorama por linguagem de programação
gold_by_language = (
    df.groupBy("language")
    .agg(
        F.count("*").alias("total_repos"),
        F.sum("stars").alias("total_stars"),
        F.avg("github_health_pct").alias("health_medio_pct"),
    )
    .orderBy(F.desc("total_repos"))
)
gold_by_language.write.format("delta").mode("overwrite").save(GOLD_PATH + "por_linguagem/")

# 3) Top 20 repositórios mais populares e ativos (não arquivados)
gold_top_repos = (
    df.filter(F.col("archived") == False)
    .orderBy(F.desc("stars"))
    .select(
        "full_name", "language", "ai_category", "stars", "forks",
        "github_health_pct", "maintenance_status", "popularity_tier",
    )
    .limit(20)
)
gold_top_repos.write.format("delta").mode("overwrite").save(GOLD_PATH + "top_repos/")

print("Agregação Gold concluída — 3 tabelas prontas para o Power BI")
