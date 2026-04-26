# Databricks notebook source
# "order_date",
# "total_orders",
# "total_revenue",
# "avg_order_value",
# "unique_customers",
# "unique_restaurants",
# "dine_in_orders",
# "takeaway_orders",
# "delivery_orders",

# COMMAND ----------

df = spark.table("dbx_az_projects.`02_silver`.fact_orders")
df.display()

# COMMAND ----------

import pyspark.sql.functions as F

# COMMAND ----------

summary  =(df
           .groupBy("order_date")
           .agg(
               F.countDistinct("order_id").alias("total_orders"),
               F.sum("total_amount").alias("total_revenue"),
               F.avg("total_amount").alias("avg_order_value"),
               F.countDistinct("customer_id").alias("unique_customers"),
               F.countDistinct("restaurant_id").alias("unique_restaurant"),
               F.sum(
                   F.when(F.col("order_type") == "delivery", 1).otherwise(0)
               ).alias("delivery_orders"),
               F.sum(
                   F.when(F.col("order_type") == "takeaway", 1).otherwise(0)
               ).alias("takeaway_orders"),
               F.sum(
                   F.when(F.col("order_type") == "dine_in", 1).otherwise(0)
               ).alias("dine_in_orders")
           ))
summary.display()

# COMMAND ----------

# "order_date",
# "total_orders",
# "total_revenue",
# "avg_order_value",
# "unique_customers",
# "unique_restaurants",
# "dine_in_orders",
# "takeaway_orders",
# "delivery_orders",
