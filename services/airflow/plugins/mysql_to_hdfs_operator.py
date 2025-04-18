from typing import Any

from airflow.operators.python import BaseOperator
from airflow.utils.context import Context
from airflow.plugins_manager import AirflowPlugin
from airflow.providers.mysql.hooks.mysql import MySqlHook
import logging
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.fs
import subprocess
from utils.spark_connections import get_spark_thrift_conn

_logger = logging.getLogger(__name__)

class MySQLToHDFSOperator(BaseOperator):
    def __init__(
            self,
            mysql_conn_id="mysql_conn_id",
            spark_conn_id=None,
            hdfs_path=None,
            schema=None,
            sql: str = None,
            params: dict = None,
            *args,
            **kwargs
    ):
        super(MySQLToHDFSOperator, self).__init__(*args, **kwargs)
        self.mysql_conn_id = mysql_conn_id
        self.spark_conn_id = spark_conn_id
        self.hdfs_path = hdfs_path
        self.schema = schema
        self.sql = sql
        self.params = params

    def get_spark_conn(self):
        conn = get_spark_thrift_conn(self.spark_conn_id)
        return conn

    def fetch_data(self, mysql_conn_id, schema, sql):
        logging.info(f"Using mysql connection id: {mysql_conn_id} with schema {schema}")
        mysql_hook = MySqlHook(mysql_conn_id=mysql_conn_id, schema=schema)
        mysql_conn = mysql_hook.get_conn()
        logging.info(f"Connect to mysql successfully!")

        cursor = mysql_conn.cursor()
        if sql is None:
            cursor.close()
            mysql_conn.close()
            raise ValueError("ERROR: SQL query cannot be None")
        

        logging.info(f"Executing query: {sql}")
        cursor.execute(sql)

        # fetch data and column names
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        logging.info(f"Fetching data successfully!")

        # close the cursor and connection
        cursor.close()
        mysql_conn.close()

        return data, column_names  # Return both data and column names

    def execute(self, context: Context) -> Any:
        data = []
        column_names = []
        
        try:
            data, column_names = self.fetch_data(
                mysql_conn_id=self.mysql_conn_id,
                schema=self.schema,
                sql=self.sql
            )
            data = list(zip(*data))  # Transpose the data to match column names
            logging.info(f"data: {data}")
            logging.info(f"columns_names: {column_names}")
        except Exception as e:
            logging.error(e)

        table = pyarrow.table(data, names = column_names)
        
        _logger.info(f"Write data to hdfs: {self.hdfs_path}")
        # Connect to HDFS
        hdfs = pa.fs.HadoopFileSystem('namenode', port=8020)

        parent_dir = self.hdfs_path.rsplit("/", 1)[0]

        # Check if directory exists, if not, create it
        if not hdfs.get_file_info(parent_dir).type == pa.fs.FileType.Directory:
            hdfs.create_dir(parent_dir)

        # Open HDFS output stream
        with hdfs.open_output_stream(self.hdfs_path) as out_stream:
            pq.write_table(table, out_stream)
        
        _logger.info(f"Write data to hdfs successfully!")


class MySQLToHDFSOperatorPlugin(AirflowPlugin):
    name = "mysql_to_hdfs_operator_plugin"
    operators = [MySQLToHDFSOperator]
