ALTER USER new_user_2 WITH LOGIN = new_user_2;


SELECT dp.name AS UserName, dp.type_desc AS UserType, sp.name AS LoginName
FROM sys.database_principals dp
JOIN sys.server_principals sp ON dp.sid = sp.sid
WHERE dp.name = 'new_user_2';


select name, type_desc,sid from sys.database_principals


select sid, name from sys.server_principals



-- Generated: 2026-04-14 07:17:19
-- Database: restaurent_db
-- User: new_user_2

-- NOTE: Azure SQL Database detected - USE statements omitted
-- Ensure you are connected to the correct database: restaurent_db
-- Current database: SELECT DB_NAME() AS CurrentDatabase;

-- CONFIGURATION FIX - Grant Execute Permissions on Utility Objects
-- This fixes missing permissions for utility stored procedures and functions
-- Error details: The EXECUTE permission was denied on the object 'lakeflowUtilityVersion_1_5', database 'restaurent_db', schema 'dbo'.


-- Grant EXECUTE permissions on all utility objects
GRANT EXECUTE ON [dbo].[lakeflowFixPermissions] TO [new_user_2];
GRANT EXECUTE ON [dbo].[lakeflowSetupChangeTracking] TO [new_user_2];
GRANT EXECUTE ON [dbo].[lakeflowSetupChangeDataCapture] TO [new_user_2];
GRANT EXECUTE ON [dbo].[lakeflowDetectPlatform] TO [new_user_2];
GRANT EXECUTE ON [dbo].[lakeflowUtilityVersion_1_5] TO [new_user_2];

PRINT 'CONFIGURATION FIX: Granted EXECUTE permissions on utility objects to user: new_user_2';
PRINT 'Re-run validation to verify permissions';


-- Azure SQL Database Platform Notes:
-- • Connect directly to the target database instead of using USE statements
-- • Server-scoped permissions may require Azure administrator access
-- • Consider using database roles for broader access patterns
