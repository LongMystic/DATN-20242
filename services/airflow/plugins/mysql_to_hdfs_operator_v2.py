from typing import Any

from airflow.operators.python import BaseOperator
from airflow.utils.context import Context
from airflow.plugins_manager import AirflowPlugin
from utils.spark_connections import get_spark_session
from airflow.hooks.base import BaseHook

import logging

_logger = logging.getLogger(__name__)

class MySQLToHDFSOperatorV2(BaseOperator):
    def __init__(
        self,
        mysql_conn_id="mysql_conn_id",
        hdfs_path=None,
        schema=None,
        table=None,
        sql: str = None,
        jdbc_options: dict = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.mysql_conn_id = mysql_conn_id
        self.hdfs_path = hdfs_path
        self.schema = schema
        self.table = table
        self.sql = sql
        self.jdbc_options = jdbc_options or {}


    def execute(self, context: Context) -> Any:
        spark = get_spark_session()

        _logger.info(f"Using MySQL connection id: {self.mysql_conn_id} with schema {self.schema}")
        _logger.info(f"Reading from MySQL using Spark with connection: {self.mysql_conn_id}")

        # Build JDBC URL from Airflow connection
        mysql_conn = BaseHook.get_connection(self.mysql_conn_id)

        jdbc_url = f"jdbc:mysql://{mysql_conn.host}:{mysql_conn.port}/{self.schema}"
        jdbc_properties = {
            "user": mysql_conn.login,
            "password": mysql_conn.password,
            "driver": "com.mysql.cj.jdbc.Driver"
        }
        jdbc_properties.update(self.jdbc_options)

        if self.sql:
            df = spark.read \
                .format("jdbc") \
                .option("url", jdbc_url) \
                .option("driver", jdbc_properties["driver"]) \
                .option("user", jdbc_properties["user"]) \
                .option("password", jdbc_properties["password"]) \
                .option("query", self.sql) \
                .load()
        else:
            raise ValueError("ERROR: SQL query cannot be None")
            

        _logger.info(f"Writing DataFrame to HDFS path: {self.hdfs_path}")
        df.write.mode("overwrite").parquet(self.hdfs_path)

        _logger.info("Data successfully written to HDFS as Parquet.")


class MySQLToHDFSOperatorV2Plugin(AirflowPlugin):
    name = "mysql_to_hdfs_operator_v2_plugin"
    operators = [MySQLToHDFSOperatorV2]