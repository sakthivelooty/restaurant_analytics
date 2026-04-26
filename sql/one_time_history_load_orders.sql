INSERT INTO dbx_az_projects.`01_bronze`.orders(
  ORDER_ID,
  TIMESTAMP,
  restaurant_id,
  customer_id,
  order_type,
  items,
  total_amount,
  payment_method,
  order_status,
  created_at
)
SELECT 
  ORDER_ID,
  order_timestamp AS `TIMESTAMP`,
  restaurant_id,
  customer_id,
  order_type,
  items,
  total_amount,
  payment_method,
  order_status,
  created_at
FROM dbx_az_projects.`01_bronze`.historical_orders;