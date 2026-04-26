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
    name = "02_silver.fact_orders",
    table_properties = {
        "quality":"silver"
    }
)
@dp.expect_all_or_drop(
    {
        "valid_order_id": "order_id IS NOT NULL",
        "valid_timestamp": "orders_timestamp IS NOT NULL",
        "valid_restaurant_id": "restaurant_id IS NOT NULL",
        "valid_customer_id": "customer_id IS NOT NULL",
        "valid_item_count": "item_count > 0",
        "valid_STATUS": "order_status in ('completed','pending','ready','delivered','preparing','confirmed')",
        "valid_payment_method": "payment_method in ('card','cash','wallet')",
        "valid_total_amount": "total_amount > 0",
    }
)
def fact_orders():

    fact_order = (
        spark.readStream.table("`01_bronze`.orders")
        .withColumn("orders_timestamp", F.to_timestamp(F.col('timestamp')))
        .withColumn("order_date", F.to_date(F.col("orders_timestamp")))
        .withColumn("order_hour", F.hour(F.col("orders_timestamp")))
        .withColumn("day_of_week", F.date_format(F.col('order_date'), 'E').cast('string'))
        .withColumn("is_weekend", F.when(F.col('day_of_week').isin(['Sat', 'Sun']), 1).otherwise(0))
        .withColumn("items_parsed", F.from_json(F.col('items'), order_item_schema))
        .withColumn("item_count", F.size(F.col('items_parsed')))
        .select(
            "order_id",
            "orders_timestamp",
            "order_date",
            "order_hour",
            "day_of_week",
            "is_weekend",
            "restaurant_id",
            "customer_id",
            "order_type",
            "item_count",
            F.col("total_amount").cast('Decimal(10,2)').alias("total_amount"),
            "payment_method",
            "order_status"
        )

    )

    return fact_order