select * from dbx_az_projects.`03_gold`.customer_profile
where customer_join_date between :date_range.min and :date_range.max