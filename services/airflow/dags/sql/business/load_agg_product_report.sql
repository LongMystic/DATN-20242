INSERT OVERWRITE TABLE iceberg.sales_business.product_report
SELECT
  sf.`date`,
  sf.item_nbr,
  i.family as product_family,
  i.class as product_class,
  i.perishable,
  SUM(sf.unit_sales) as total_sales
FROM sales_business.sales_fact sf
LEFT JOIN sales_business.items_dim i ON sf.item_nbr = i.item_nbr
GROUP BY 
  sf.`date`,
  sf.item_nbr,
  i.family,
  i.class,
  i.perishable 