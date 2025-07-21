from typing import Any, List, Dict
from airflow.operators.python import BaseOperator
from airflow.utils.context import Context
from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base import BaseHook
import pymysql
import logging

_logger = logging.getLogger(__name__)

class GetBatchInfoOperator(BaseOperator):
    """
    Connects to MySQL to find the min and max of a partition column and
    generates a list of batch boundaries.
    """
    def __init__(
        self,
        mysql_conn_id: str = "mysql_conn_id",
        schema: str = None,
        table: str = None,
        sql: str = None,
        params: dict = {},
        partition_column: str = None,
        batch_size: int = 500000,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.mysql_conn_id = mysql_conn_id
        self.schema = schema
        self.table = table
        self.sql = sql
        self.params = params
        self.partition_column = partition_column
        self.batch_size = batch_size

    def execute(self, context: Context) -> List[Dict[str, Any]]:
        mysql_conn = BaseHook.get_connection(self.mysql_conn_id)
        mysql_connection = pymysql.connect(
            host=mysql_conn.host,
            port=mysql_conn.port,
            user=mysql_conn.login,
            password=mysql_conn.password,
            database=self.schema
        )
        mysql_cursor = mysql_connection.cursor()

        if self.sql is None or self.sql == "":
            base_query = f"SELECT * FROM {self.schema}.{self.table}"
        else:
            self.sql = f"/opt/airflow/dags{self.sql}"
            with open(self.sql, 'r') as f:
                base_query = f.read()
                for param in self.params:
                    base_query = base_query.replace(f"{{{param}}}", self.params[param])
        
        _logger.info(f"Executing base query for min/max: {base_query}")

        min_max_query = f"""
            SELECT MIN({self.partition_column}) as min_val, 
                   MAX({self.partition_column}) as max_val 
            FROM ({base_query}) as base
        """
        mysql_cursor.execute(min_max_query)
        min_val, max_val = mysql_cursor.fetchone()
        
        if min_val is None or max_val is None:
            _logger.warning(f"No data found for table {self.table}. Returning empty batch list.")
            return []

        _logger.info(f"Min value: {min_val}, Max value: {max_val}")

        total_rows = max_val - min_val + 1
        num_batches = (total_rows + self.batch_size - 1) // self.batch_size
        _logger.info(f"Calculated {num_batches} batches for {total_rows} rows.")

        batches = []
        for batch_num in range(num_batches):
            start_val = min_val + (batch_num * self.batch_size)
            end_val = min(start_val + self.batch_size - 1, max_val)
            batches.append({
                "batch_num": batch_num,
                "start_val": start_val,
                "end_val": end_val
            })
        
        mysql_cursor.close()
        mysql_connection.close()

        _logger.info(f"Returning {len(batches)} batches to be processed.")
        return batches

class GetBatchInfoOperatorPlugin(AirflowPlugin):
    name = "get_batch_info_operator_plugin"
    operators = [GetBatchInfoOperator] 