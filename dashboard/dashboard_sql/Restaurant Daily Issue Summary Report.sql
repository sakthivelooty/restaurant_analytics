select 
rst.name as restaurant_name,
date(fr.review_timestamp) as date,

sum(
    case 
        when issue_delivery = 'true' then 1
        else 0
    end
) as delivery_issues,

sum(
    case 
        when issue_food_quality = 'true' then 1
        else 0
    end
) as food_quality_issue,
sum(
    case 
        when issue_pricing = 'true' then 1
        else 0
    end
) as pricing_issues,
sum(
    case 
        when issue_portion_size = 'true' then 1
        else 0
    end
) as portion_size_issue
from dbx_az_projects.`02_silver`.fact_reviews fr
join dbx_az_projects.`02_silver`.dim_resturants rst on rst.restaurant_id = fr.restaurant_id
group by 1, 2