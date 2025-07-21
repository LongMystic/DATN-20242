INSERT OVERWRITE TABLE {iceberg_db}.sales_limit_fact
SELECT
    id,
    date,
    store_nbr,
    item_nbr,
    unit_sales,
    onpromotion
FROM {iceberg_db_stg}.sales_limit
