# test_data_quality.py
# Testes básicos de qualidade de dados (esqueleto — expandir com Great Expectations)

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("data_quality_tests").getOrCreate()


def test_silver_no_duplicate_repos():
    df = spark.read.format("delta").load("data/silver/repos/")
    assert df.count() == df.dropDuplicates(["full_name"]).count(), "Existem repositórios duplicados na Silver"


def test_silver_stars_not_negative():
    df = spark.read.format("delta").load("data/silver/repos/")
    assert df.filter(df.stars < 0).count() == 0, "Existem valores negativos de stars"


def test_gold_tables_not_empty():
    for table in ["por_categoria", "por_linguagem", "top_repos"]:
        df = spark.read.format("delta").load(f"data/gold/{table}/")
        assert df.count() > 0, f"Tabela Gold '{table}' está vazia"
