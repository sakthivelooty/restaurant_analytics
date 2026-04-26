from pyspark import pipelines as dp
import pyspark.sql.functions as F

@dp.materialized_view(
    name = "03_gold.dim_restaurant_review",
    table_properties = {"quality": "gold"}
)
def dim_restaurant_review():
    review = spark.table("dbx_az_projects.`02_silver`.fact_reviews")
    rest = spark.table("dbx_az_projects.`02_silver`.dim_resturants")

    review_stats = (
        review
        .groupBy("restaurant_id")
        .agg(
            F.countDistinct("review_id").alias("total_reviews"),
            F.round(F.avg("rating")).alias("avg_rating"),

            F.sum(F.when(F.col("rating") == 5, 1).otherwise(0)).alias("rating_5_count"),
            F.sum(F.when(F.col("rating") == 4, 1).otherwise(0)).alias("rating_4_count"),
            F.sum(F.when(F.col("rating") == 3, 1).otherwise(0)).alias("rating_3_count"),
            F.sum(F.when(F.col("rating") == 2, 1).otherwise(0)).alias("rating_2_count"),
            F.sum(F.when(F.col("rating") == 1, 1).otherwise(0)).alias("rating_1_count"),

            F.sum(F.when(F.col("sentiment") == "positive", 1).otherwise(0)).alias("sentiment_positive_count"),
            F.sum(F.when(F.col("sentiment") == "neutral", 1).otherwise(0)).alias("sentiment_neutral_count"),
            F.sum(F.when(F.col("sentiment") == "negative", 1).otherwise(0)).alias("sentiment_negative_count"),
            )
    )

    rest_review_stats = (
                    rest
                     .join(review_stats, "restaurant_id", "left")
                     .select(
                        F.col("restaurant_id"),
                        F.col("name").alias("restaurant_name"),
                        rest.city,

                        F.col("total_reviews"),
                        F.col("avg_rating"),
                        F.col("rating_5_count"),
                        F.col("rating_4_count"),
                        F.col("rating_3_count"),
                        F.col("rating_2_count"),
                        F.col("rating_1_count"),
                        F.col("sentiment_positive_count"),
                        F.col("sentiment_neutral_count"),
                        F.col("sentiment_negative_count")
                    )
                )
    return rest_review_stats