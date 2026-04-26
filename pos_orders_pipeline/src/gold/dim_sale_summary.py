from pyspark import pipelines as dp
import pyspark.sql.functions as F

@dp.materialized_view(
    name = "03_gold.dim_sales_summary",
    table_properties = {"quality": "gold"},
    partition_cols = ["order_date"]
)
def dim_sales_summary():
  df = (
      spark.read.table("`02_silver`.fact_orders")
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
           )
        )
  return df
