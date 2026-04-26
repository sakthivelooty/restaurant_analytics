
-- https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view
select 

restaurant_name,
rating_lable,
rating_count
from dbx_az_projects.`03_gold`.dim_restaurant_review
lateral view STACK(
    5,
    "5 STAR", rating_5_count,
    "4 STAR", rating_4_count,
    "3 STAR", rating_3_count,
    "2 STAR", rating_2_count,
    "1 STAR", rating_1_count
) AS rating_lable, rating_count

-- "rest_name", "rating_lable", 'rating_count'