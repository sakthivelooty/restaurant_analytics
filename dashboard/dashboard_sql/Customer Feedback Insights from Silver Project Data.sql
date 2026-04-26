select 
rst.name as restaurant_name, 
date(review_timestamp) as review_date,
review_text as rating 
from dbx_az_projects.`02_silver`.fact_reviews fr
join dbx_az_projects.`02_silver`.dim_resturants rst on rst.restaurant_id = fr.restaurant_id
where sentiment = 'positive'
order by review_date desc
