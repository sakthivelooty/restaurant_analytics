select * from dbx_az_projects.`03_gold`.dim_sales_summary
where order_date between :date_range.min and :date_range.max
