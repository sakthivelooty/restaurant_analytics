CREATE LOGIN new_user WITH PASSWORD = 'Welcome@1234';


CREATE USER new_user FOR LOGIN new_user;

GRANT CONNECT TO new_user;

GRANT SELECT ON sys.databases TO new_user;

-- bug fix
ALTER USER new_user WITH LOGIN = new_user;