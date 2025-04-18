from airflow.plugins_manager import AirflowPlugin
from utils.spark_connections import get_spark_thrift_conn
from airflow.models import BaseOperator
from utils.utils import generate_create_table_sql

import logging

_logger = logging.getLogger(__name__)

class HDFSToIcebergOperator(BaseOperator):
    def __init__(
            self,
            task_id: str = "",
            spark_conn_id: str=None,
            iceberg_table_name:str =None,
            num_keep_retention_snaps=5,
            iceberg_db="default",
            table_properties=None,
            *args,
            **kwargs
    ):
        super().__init__(task_id=task_id)
        self.spark_conn_id = spark_conn_id
        self.iceberg_table_name = iceberg_table_name
        self.num_keep_retention_snaps = num_keep_retention_snaps
        self.iceberg_db = iceberg_db
        self.table_properties = table_properties

    def get_spark_conn(self):
        conn = get_spark_thrift_conn(self.spark_conn_id)
        return conn

    # def create_tmp_table(self, cursor):
    #     drop_tmp_table_sql = f"""
    #         DROP TABLE IF EXISTS default.{self.iceberg_table_name}_tmp
    #     """
    #     _logger.info("\nDropping tmp table if exists\n")
    #     cursor.execute(drop_tmp_table_sql)
    #
    #     create_tmp_table_sql = f"""
    #         CREATE TABLE default.{self.iceberg_table_name}_tmp
    #         USING parquet
    #         LOCATION '/raw/{self.iceberg_table_name}_tmp/'
    #     """
    #
    #     _logger.info("\nCreating tmp table\n")
    #     cursor.execute(create_tmp_table_sql)

    def insert_data_into_staging_table(self, cursor):
        insert_data_sql = f"""
            INSERT INTO {self.iceberg_db}.{self.iceberg_table_name}
            SELECT *
            FROM default.{self.iceberg_table_name}_tmp
        """

        _logger.info("\nInserting data into staging table\n")
        cursor.execute(insert_data_sql)

    def create_staging_table(self, cursor):
        create_database_query_sql = f"""
            CREATE DATABASE IF NOT EXISTS {self.iceberg_db}
        """
        _logger.info("\nCreating database if not exists\n")
        cursor.execute(create_database_query_sql)


        drop_staging_table_sql = f"""
            DROP TABLE IF EXISTS {self.iceberg_db}.{self.iceberg_table_name};
        """
        _logger.info("\nDropping staging table\n")
        cursor.execute(drop_staging_table_sql)
        create_staging_table_sql = generate_create_table_sql(
            iceberg_db=self.iceberg_db,
            iceberg_table=self.iceberg_table_name,
            iceberg_columns_properties=self.table_properties,
            location=f"/raw/{self.iceberg_db}/{self.iceberg_table_name}/"
        )

        _logger.info("\nCreating staging table\n")
        cursor.execute(create_staging_table_sql)

    def drop_tmp_table(self, cursor):
        drop_tmp_table_sql = f"""
            DROP TABLE IF EXISTS default.{self.iceberg_table_name}_tmp
        """

        _logger.info("\nDropping tmp table\n")
        cursor.execute(drop_tmp_table_sql)

    def execute(self, context):
        conn = self.get_spark_conn()
        cursor = conn.cursor()

        if self.iceberg_table_name is None:
            cursor.close()
            conn.close()
            raise ValueError("Iceberg table name is not provided.")
        else:
            _logger.info(f"Using iceberg table name: {self.iceberg_table_name}")
            _logger.info(f"Using iceberg db: {self.iceberg_db}")    
            # self.create_tmp_table(cursor)
            self.create_staging_table(cursor)
            self.insert_data_into_staging_table(cursor)
            self.drop_tmp_table(cursor)
            cursor.close()
            conn.close()
            _logger.info("Data transfer completed successfully.")

        
class HDFSToIcebergPlugin(AirflowPlugin):
    name = "hdfs_to_iceberg_plugin"
    operators = [HDFSToIcebergOperator]