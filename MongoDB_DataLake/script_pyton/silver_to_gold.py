from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("Silver_to_Gold")
    .master("local[*]")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

from pyspark.sql.functions import col

df_silver = spark.read.parquet(
    r"C:\Professional_project\MongoDB_DataLake\temp\silver"
)

fact_transactions = df_silver.select(

    col("step"),

    col("transaction_amount"),

    col("transaction_type"),

    col("origin_account_id"),

    col("origin_balance_before"),

    col("origin_balance_after"),

    col("destination_account_id"),

    col("destination_balance_before"),

    col("destination_balance_after"),

    col("is_fraud"),

    col("is_flagged")

)

gold_path = r"C:\Professional_project\MongoDB_DataLake\temp\gold\fact_transactions"

fact_transactions.write \
    .format("delta") \
    .mode("overwrite") \
    .save(gold_path)