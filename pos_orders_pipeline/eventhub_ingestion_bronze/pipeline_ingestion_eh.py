# scripts as per the dicument: https://docs.databricks.com/aws/en/ldp/event-hubs

from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark import pipelines as dp

EH_CONN_STR = ""
EH_NAME = ""
EH_NAMESPACE = ""

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

@dp.table(name="orders", table_properties={"quality": "bronze"})
def orders():
    df_raw = (
        spark.readStream.format("kafka")
        .options(**KAFKA_OPTIONS)
        .load()
    )
    df_raw_updated =( df_raw
                 .withColumn("key", F.col("key").cast("string"))
                 .withColumn("value", F.col("value").cast("string"))
                 .withColumn("data", F.from_json(F.col("value"), orders_schema))
                 .select("data.*")
    )
    return df_raw_updated