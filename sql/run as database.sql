CREATE USER new_user FOR LOGIN new_user;

EXEC dbo.lakeflowFixPermissions 
  @User = 'new_user', 
  @Tables = 'ALL';

-- Enable CDC on all user tables and grant CDC access to the ingestion user
EXEC dbo.lakeflowSetupChangeDataCapture 
  @Tables = 'ALL', 
  @User = 'new_user';


GRANT SELECT ON SCHEMA::dbo TO new_user;


ALTER USER new_user WITH LOGIN = new_user;