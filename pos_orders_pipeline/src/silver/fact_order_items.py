from pyspark import pipelines as dp
import pyspark.sql.functions as F
from pyspark.sql.types import *

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

@dp.table(
    name = "02_silver.fact_order_items",
    table_properties = {
        "quality":"silver"
    }
)
def fact_order_items():

    fact_order_items = (
        spark.readStream.table("`01_bronze`.orders")
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
                  F.col("items.subtotal").cast("decimal(10,2)").alias("subtotal"),
            )
            )

    return fact_order_items