
-- Put on the "mask" of the ingestion user
EXECUTE AS USER = 'new_user';


-- This is what Databricks queries during Schema Exploration. 
SELECT name AS TableName, is_tracked_by_cdc 
FROM sys.tables 
WHERE is_tracked_by_cdc = 1;

