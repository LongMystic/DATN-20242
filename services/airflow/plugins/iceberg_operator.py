from utils.spark_connections import get_spark_thrift_conn
from airflow.models import BaseOperator

class IcebergOperator(BaseOperator):
    def __init__(
            self, task_id: str,
            hive_server2_conn_id,
            sql="",
            iceberg_table_name=None,
            iceberg_table_uri=None,
            iceberg_table_props=None,
            num_keep_retention_snaps=None,
            iceberg_db="default",
            *args,
            **kwargs
    ):
        super().__init__(task_id, *args, **kwargs)
        self.hive_server2_conn_id = hive_server2_conn_id
        self.sql = sql
        self.iceberg_table_name = iceberg_table_name
        self.iceberg_table_uri = iceberg_table_uri
        self.iceberg_table_props = iceberg_table_props
        self.num_keep_retention_snaps = num_keep_retention_snaps
        self.iceberg_db = iceberg_db

