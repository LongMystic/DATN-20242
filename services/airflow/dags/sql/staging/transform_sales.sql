INSERT OVERWRITE TABLE {iceberg_db}.sales_fact
SELECT *
FROM {iceberg_db_stg}.sales
