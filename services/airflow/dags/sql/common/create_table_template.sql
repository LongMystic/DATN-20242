CREATE TABLE IF NOT EXISTS {iceberg_db}.{iceberg_table} (
    {iceberg_columns_properties}
)
USING iceberg
LOCATION {location}
tblproperties (
  'format' = 'iceberg/parquet',
  'format-version' = '1',
  'write.format.default' = 'parquet',
  'write.metadata.previous-versions-max' = '2',
  'write.parquet.compression-codec' = 'snappy',
  'external.table.purge' = 'true'
 )