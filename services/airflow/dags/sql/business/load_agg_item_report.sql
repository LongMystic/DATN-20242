INSERT OVERWRITE TABLE iceberg.sales_business.item_report
SELECT 
  `date`,
  sf.item_nbr,
  family,
  class,
  perishable,
  city,
  unit_sales
FROM sales_business.sales_limit_fact sf
LEFT JOIN sales_business.stores_dim st on sf.store_nbr = st.store_nbr
LEFT JOIN sales_business.items_dim i on sf.item_nbr = i.item_nbr