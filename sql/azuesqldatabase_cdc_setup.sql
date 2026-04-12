
-- Part 2 - 
-- Now run projects/databricks-e2e-project/sql/utility_script.sql
-- https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/sql-server-utility

ALTER DATABASE restaurent_db SET CHANGE_TRACKING = ON (CHANGE_RETENTION = 14 DAYS, AUTO_CLEANUP = ON);

-- Note: replace 'dbo' with the schema you're using
ALTER TABLE dbo.customers ENABLE CHANGE_TRACKING;
ALTER TABLE dbo.historical_orders ENABLE CHANGE_TRACKING;
ALTER TABLE dbo.menu_items ENABLE CHANGE_TRACKING;
ALTER TABLE dbo.restaurants ENABLE CHANGE_TRACKING;
ALTER TABLE dbo.reviews ENABLE CHANGE_TRACKING;

EXEC sys.sp_cdc_enable_db;

EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name   = N'customers',
    @role_name     = NULL;
GO;

EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name   = N'historical_orders',
    @role_name     = NULL;
GO;

EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name   = N'menu_items',
    @role_name     = NULL;
GO;

EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name   = N'restaurants',
    @role_name     = NULL;
GO;

EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name   = N'reviews',
    @role_name     = NULL;
GO;

EXEC dbo.lakeflowFixPermissions
    @User = 'databrickse2eprojUserAdmin',
    @Tables = 'ALL';

EXEC dbo.lakeflowSetupChangeTracking
    @Tables = 'ALL',
    @User = '**uName**';

-- Enable CDC on specific tables
EXEC dbo.lakeflowSetupChangeDataCapture
    @Tables = 'ALL',
    @User = '**PWD**';

---------------
-- CDC Commands
---------------
update customers
set city='Abu Dhabi'
where customer_id='CUST-10000';

insert into dbo.menu_items (restaurant_id, item_id, name, category, price, ingredients, is_vegetarian, spice_level)
values ('REST-AUH-001','ITEM-999','Samosa (2 pcs)','Starter',18.49,'Potato, Peas, Spices, Pastry',1,'Medium');