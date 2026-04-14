CREATE USER new_user_2 FOR LOGIN new_user_2;

-- Enable change tracking on specific tables
EXEC dbo.lakeflowSetupChangeTracking
    @Tables = 'dbo.customers',
    @User = 'new_user_2',
    @Retention = '2 DAYS';

GRANT SELECT ON dbo.historical_orders TO new_user_2;
GRANT SELECT ON dbo.customers TO new_user_2;

EXEC dbo.lakeflowSetupChangeTracking
    @Tables = '[dbo].[menu_items]',
    @User = 'new_user_2',
    @Retention = '2 DAYS';

GRANT SELECT ON [dbo].[menu_items] TO new_user_2;

EXEC dbo.lakeflowSetupChangeTracking
    @Tables = '[dbo].[restaurants]',
    @User = 'new_user_2',
    @Retention = '2 DAYS';

GRANT SELECT ON [dbo].[restaurants] TO new_user_2;

EXEC dbo.lakeflowSetupChangeTracking
    @Tables = '[dbo].[reviews]',
    @User = 'new_user_2',
    @Retention = '2 DAYS';

GRANT SELECT ON [dbo].[reviews] TO new_user_2;


GRANT VIEW DATABASE STATE TO new_user_2;

GRANT VIEW DEFINITION TO new_user_2