select 
    rest.name as resturant_name,
    date(review_timestamp) as review_date,
    sum(
        case 
         when sentiment = 'negative' then 1
         else 0
        end 
    ) as negative_review_count,
    sum(
        case 
         when sentiment = 'positive' then 1
         else 0
        end 
    ) as positive_review_count,
    sum(
        case 
         when sentiment = 'neutral' then 1
         else 0
        end 
    ) as neutral_review_count
from dbx_az_projects.`02_silver`.fact_reviews review
join dbx_az_projects.`02_silver`.dim_resturants rest on rest.restaurant_id = review.restaurant_id
group by  1,2