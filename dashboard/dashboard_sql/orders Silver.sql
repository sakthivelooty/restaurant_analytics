select * from dbx_az_projects.`02_silver`.fact_orders
where order_date between :date_range.min and :date_range.max