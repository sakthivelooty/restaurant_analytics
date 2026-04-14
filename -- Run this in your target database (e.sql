-- Run this in your target database (e.g., restaurent_db)
CREATE LOGIN new_user_2
WITH PASSWORD = 'Welcome@123';

-- 2. Switch to your target database
USE restaurent_db;


GRANT VIEW SERVER STATE TO new_user_2;

-- 3. Create the database user mapped to the login
CREATE USER new_user_2 FOR LOGIN new_user_2;

grant connect to new_user_2;


ALTER SERVER ROLE ##MS_ServerStateReader## ADD MEMBER new_user_2;

ALTER SERVER ROLE ##MS_DefinitionReader## ADD MEMBER new_user_2;


SELECT 
    dp.name AS UserName, 
    dp.type_desc AS UserType,
    -- sp.name AS LoginName
FROM sys.database_principals dp
JOIN sys.server_principals sp ON dp.sid = sp.sid
WHERE dp.name = 'new_user_2';

select name,  type_desc,sid FROM sys.database_principals dp

select sid, name from sys.server_principals;

ALTER USER new_user_2 WITH LOGIN = new_user_2;