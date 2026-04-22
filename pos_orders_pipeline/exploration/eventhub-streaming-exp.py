# Databricks notebook source
from pyspark.sql.types import *
import pyspark.sql.functions as F

# COMMAND ----------

EH_CONN_STR = ""
EH_NAME = ""
EH_NAMESPACE = ""

# COMMAND ----------

KAFKA_OPTIONS = {
  "kafka.bootstrap.servers"  : f"{EH_NAMESPACE}.servicebus.windows.net:9093",
  "subscribe"                : EH_NAME,
  "kafka.sasl.mechanism"     : "PLAIN",
  "kafka.security.protocol"  : "SASL_SSL",
  "kafka.sasl.jaas.config"   : f"kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username=\"$ConnectionString\" password=\"{EH_CONN_STR}\";",
  "kafka.request.timeout.ms" : "60000",
  "kafka.session.timeout.ms" : "30000",
  "maxOffsetsPerTrigger"     : "5000",
  "failOnDataLoss"           : "false",
  "startingOffsets"          : "earliest"
}

# COMMAND ----------

df_raw = (
    spark.readStream.format("kafka")
    .options(**KAFKA_OPTIONS)
    .load()
)


# COMMAND ----------


orders_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("restaurant_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("order_type", StringType(), True),
    StructField("items", StringType(), True),
    StructField("total_amount", DoubleType(), True),
    StructField("payment_method", StringType(), True),
    StructField("order_status", StringType(), True),
    StructField("created_at", StringType(), True)
])


# COMMAND ----------

df_raw_updated =( df_raw
                 .withColumn("key", F.col("key").cast("string"))
                 .withColumn("value", F.col("value").cast("string"))
                 .withColumn("data", F.from_json(F.col("value"), orders_schema))
                 .select("data.*")
    )

# COMMAND ----------


display(df_raw_updated ,checkpointLocation= "/Volumes/dbx_az_projects/default/testing_checkpoint/checkpoints_6")

# COMMAND ----------


