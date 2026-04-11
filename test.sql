-- bcp restaurent_ops.dbo.customers in "/home/sakthi/dbx_projects/restaurant_analytics/00_synthetic_data/data/customers.csv" -S restsqlserverops.database.windows.net -U admin_dbx_azure -P Whiskey@Smiles005 -d restaurent_ops -c -t ","


select count(*) from [dbo].[customers];