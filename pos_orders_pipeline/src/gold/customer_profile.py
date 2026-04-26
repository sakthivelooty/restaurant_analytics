from pyspark.sql.functions import * 
from pyspark.sql.window import Window
from pyspark import pipelines as dp

@dp.materialized_view(
    name = "03_gold.customer_profile",
    table_properties={"quality": "gold"}
)
def customer_profile():

    df_customer = spark.table("dbx_az_projects.`02_silver`.dim_customer")
    df_restuarents = spark.table("dbx_az_projects.`02_silver`.dim_resturants")
    df_orders = spark.table("dbx_az_projects.`02_silver`.fact_orders")
    df_order_items = spark.table("dbx_az_projects.`02_silver`.fact_order_items")
    df_reviews = spark.table("dbx_az_projects.`02_silver`.fact_reviews")

    order_stats = (
        df_orders
        .groupBy("customer_id")
        .agg(
                countDistinct("order_id").alias("total_orders"),
                sum("total_amount").alias("total_lifetime_spend"),
                avg("total_amount").alias("avg_order_value"),
                max("order_date").alias("last_ordered_date")
            )
    )

    review_stats = (
        df_reviews
        .groupBy("customer_id")
        .agg(
            countDistinct("review_id").alias("total_review"),
            avg("rating").alias("avg_rating")
        )
    )

    favorite_restaurant = (
        df_orders
        .groupBy("customer_id","restaurant_id")
        .agg(countDistinct("order_id").alias("order_count"))
        .withColumn("rn",row_number().over(Window.partitionBy("customer_id").orderBy(desc("order_count"))))
        .filter("rn == 1")
        .join(df_restuarents, on="restaurant_id", how="left")
        .selectExpr("customer_id","restaurant_id","name as favorite_restaurant")
    )

    favorite_item = (
        df_orders.join(df_order_items, "order_id", "inner")
        .groupBy("customer_id","item_name")
        .agg(
            sum("quantity").alias("item_qty")
        )
        .withColumn("rn", row_number().over(Window.partitionBy("customer_id").orderBy(desc("item_qty"))))
        .filter("rn == 1")
        .selectExpr("customer_id","item_name as favorite_item")
    )

    df_customer_360 = (
        df_customer.join(favorite_item, "customer_id", "left")
        .join(favorite_restaurant, "customer_id", "left")
        .join(review_stats, "customer_id", "left")
        .join(order_stats, "customer_id", "left")
        .select(
            col("customer_id").alias("customer_id"),
            col("name").alias("customer_name"),
            col("email").alias("customer_email"),
            col("phone").alias("customer_phone"),
            col("city").alias("customer_city"),
            col("join_date").alias("customer_join_date"),
            #fav_items
            col("favorite_item").alias("customer_favorite_item"),
            col("favorite_restaurant").alias("customer_favorite_restaurant"),
            #order_stats
            coalesce(col("total_orders"), lit(0)).cast("bigint").alias("total_orders"),
            coalesce(col("total_lifetime_spend"), lit(0)).cast("decimal(10,2)").alias("total_lifetime_spend"),
            coalesce(col("avg_order_value"), lit(0)).cast("decimal(10,2)").alias("avg_order_value"),
            col("last_ordered_date").alias("last_ordered_date"),
            #review_stats
            coalesce(col("avg_rating"),lit(0)).cast("bigint").alias("avg_rating"),
            col("total_review").alias('total_review'),
            #loyality 
            when(
                col("total_lifetime_spend") >= 500, "Gold"
            ).when(
                col("total_lifetime_spend") >= 200, "Silver"
            ).when(
                col("total_lifetime_spend") >= 100, "Bronze"
            ).otherwise("New").alias("loyality_segment")


        
        )
    )

    return df_customer_360





