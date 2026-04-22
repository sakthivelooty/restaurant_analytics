# Databricks notebook source
orders = spark.read.table("dbx_az_projects.`01_bronze`.orders")
orders.display()

# COMMAND ----------

import pyspark.sql.functions as F
from pyspark.sql.types import *

# COMMAND ----------

order_item_schema = ArrayType(
    StructType([
        StructField("item_id", StringType()),
        StructField("name", StringType()),
        StructField("category", StringType()),
        StructField("quantity", StringType()),
        StructField("unit_price", DecimalType(10,2)),
        StructField("subtotal", DecimalType(10,2))
    ])
)

    

# COMMAND ----------

fact_orders = (
    orders
    .withColumn("orders_timestamp", F.to_timestamp(F.col('timestamp')))
    .withColumn("order_date", F.to_date(F.col("orders_timestamp")))
    .withColumn("order_hour", F.hour(F.col("orders_timestamp")))
    .withColumn("day_of_week", F.date_format(F.col('order_date'), 'E').cast('string'))
    .withColumn("is_weekend", F.when(F.col('day_of_week').isin(['Sat', 'Sun']), 1).otherwise(0))
    .withColumn("items_parsed", F.from_json(F.col('items'), order_item_schema))
    .withColumn("item_count", F.size(F.col('items_parsed')))
)
fact_orders.display()

# COMMAND ----------

fact_order_items=  (orders
                    .withColumn("orders_timestamp", F.to_timestamp(F.col('timestamp')))
                    .withColumn("order_date", F.to_date(F.col("orders_timestamp")))
                    .withColumn("items_parsed", F.from_json(F.col('items'), order_item_schema))
                    .withColumn("items", F.explode(F.col('items_parsed')))
                    .select(
                        "order_id",
                        F.col("items.item_id").alias("item_id"),
                        "restaurant_id",
                        "orders_timestamp",
                        "order_date",
                         F.col("items.name").alias("item_name"),
                        F.col("items.category").alias("category"),
                        F.col("items.quantity").alias("quantity"),
                         F.col("items.unit_price").cast("decimal(10,2)").alias("unit_price"),
                         F.col("items.subtotal").cast("decimal(10,2)").alias("quantity"),
                    )
                    )
fact_order_items.display()

# COMMAND ----------

""
