select item_name,
sum(quantity) as total_quantity 
from dbx_az_projects.`02_silver`.fact_order_items
group by item_name, order_date
having order_date between :date_range.min and :date_range.max
order by total_quantity desc
limit 10;