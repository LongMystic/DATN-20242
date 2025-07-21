from typing import Any
from datetime import datetime
from airflow.operators.python import BaseOperator
from airflow.utils.context import Context
from airflow.plugins_manager import AirflowPlugin
from utils.spark_connections import get_spark_thrift_conn
from airflow.hooks.base import BaseHook
import pymysql

import logging

_logger = logging.getLogger(__name__)


class MySQLToHDFSOperatorV3(BaseOperator):
    def __init__(
            self,
            mysql_conn_id="mysql_conn_id",
            spark_conn_id="spark_conn_id",
            hdfs_path=None,
            schema=None,
            table=None,
            sql: str = None,
            jdbc_options: dict = None,
            params: dict = {},
            partition_column: str = None,
            batch_info: dict = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.mysql_conn_id = mysql_conn_id
        self.spark_conn_id = spark_conn_id
        self.hdfs_path = hdfs_path
        self.schema = schema
        self.table = table
        self.sql = sql
        self.params = params
        self.partition_column = partition_column
        self.batch_info = batch_info

    def remove_raw_location(self, cursor):
        raw_path = f"/raw/{self.table}_tmp/{datetime.now().strftime('%Y-%m-%d')}"
        _logger.info(f"\nRemoving raw location folder: {raw_path}\n")
        try:
            # Use Spark SQL to remove the directory
            remove_path_sql = f"""
                DROP TABLE IF EXISTS default.{self.table}_tmp;
                CREATE OR REPLACE TEMPORARY VIEW temp_view_{self.table} AS SELECT 1;
                INSERT OVERWRITE DIRECTORY '{raw_path}' SELECT * FROM temp_view_{self.table};
                DROP VIEW IF EXISTS temp_view_{self.table}
            """
            for query in remove_path_sql.split(";"):
                cursor.execute(query)
            _logger.info(f"Successfully removed raw location folder: {raw_path}")
        except Exception as e:
            _logger.error(f"Failed to remove raw location folder: {e}")
            raise

    def execute(self, context: Context) -> Any:
        _logger.info(f"Using MySQL connection id: {self.mysql_conn_id} with schema {self.schema}")
        _logger.info(f"Using Spark connection id: {self.spark_conn_id}")
        _logger.info(f"Using HDFS path to write data: {self.hdfs_path}")

        # Get Spark connection
        spark_conn = get_spark_thrift_conn(self.spark_conn_id)
        spark_cursor = spark_conn.cursor()
        # self.remove_raw_location(spark_cursor)
        # Get MySQL connection
        mysql_conn = BaseHook.get_connection(self.mysql_conn_id)

        _logger.info(f"Using SQL PATH: {self.sql}")

        if self.sql is None or self.sql == "":
            _logger.info("Sql query is empty, use \"SELECT * FROM schema.table\" as default query")
            base_query = f"SELECT * FROM {self.schema}.{self.table}"
        else:
            self.sql = f"/opt/airflow/dags{self.sql}"
            with open(self.sql, 'r') as f:
                base_query = f.read()
                for param in self.params:
                    base_query = base_query.replace(f"{{{param}}}", self.params[param])
            _logger.info(f"Using SQL file: {base_query}")

        start_val = self.batch_info['start_val']
        end_val = self.batch_info['end_val']
        batch_num = self.batch_info['batch_num']
        
        _logger.info(f"Processing batch {batch_num} (IDs {start_val} to {end_val})")
        
        # Create batch-specific query
        operator = ""
        if "WHERE" in base_query:
            operator = "AND"
        else:
            operator = "WHERE"

        batch_query = f"""
            ({base_query}
                {operator} {self.partition_column} >= {start_val} 
                AND {self.partition_column} <= {end_val}
            ) as filtered_data 
        """

        # Process batch
        batch_path = f"{self.hdfs_path}/batch_{batch_num}"
        spark_query = f"""
            SET spark.sql.legacy.allowNonEmptyLocationInCTAS=true;
            
            CREATE OR REPLACE TEMPORARY VIEW {self.table}_view_{batch_num}
            USING org.apache.spark.sql.jdbc
            OPTIONS (
              url "jdbc:mysql://{mysql_conn.host}:{mysql_conn.port}/{self.schema}",
              dbtable "{batch_query}",
              user '{mysql_conn.login}',
              password '{mysql_conn.password}'
            );
            
            DROP TABLE IF EXISTS {self.table}_tmp_{batch_num};
            CREATE TABLE {self.table}_tmp_{batch_num}
            USING parquet
            OPTIONS (path '{batch_path}')
            AS SELECT * FROM {self.table}_view_{batch_num};
            
            DROP VIEW IF EXISTS {self.table}_view_{batch_num}
        """

        for query in spark_query.split(';'):
            if query.strip():
                _logger.info(f"Executing query: {query}")
                spark_cursor.execute(query)

        _logger.info(f"Completed batch {batch_num}")

        # Clean up connections
        spark_cursor.close()
        spark_conn.close()

        _logger.info(f"Successfully created parquet file in {batch_path}")


class MySQLToHDFSOperatorV3Plugin(AirflowPlugin):
    name = "mysql_to_hdfs_operator_v3_plugin"
    operators = [MySQLToHDFSOperatorV3]