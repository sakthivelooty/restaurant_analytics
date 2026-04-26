select sum(quantity * unit_price) as total_amount
,category 
from dbx_az_projects.`02_silver`.fact_order_items
group by category,order_date
having order_date between :date_range.min and :date_range.max
