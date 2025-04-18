from airflow.plugins_manager import AirflowPlugin
from utils.spark_connections import get_spark_thrift_conn
from airflow.models import BaseOperator
from datetime import datetime, timedelta
from utils.utils import generate_create_table_sql
import logging
_logger = logging.getLogger(__name__)

class IcebergOperator(BaseOperator):
    def __init__(
            self,
            task_id: str = "",
            spark_conn_id: str=None,
            sql_path="",
            iceberg_table_name=None,
            num_keep_retention_snaps=5,
            iceberg_db="default",
            table_properties=None,
            *args,
            **kwargs
    ):
        super().__init__(task_id=task_id)
        self.spark_conn_id = spark_conn_id
        self.sql_path = sql_path
        self.iceberg_table_name = iceberg_table_name
        self.num_keep_retention_snaps = num_keep_retention_snaps
        self.iceberg_db = iceberg_db
        self.table_properties = table_properties


    def get_spark_conn(self):
        conn = get_spark_thrift_conn(self.spark_conn_id)
        return conn

    def call_expire_snapshots(self, cursor):
        expire_snapshot_sql = f"""
            CALL iceberg.system.expire_snapshots (
                table => '{self.iceberg_db}.{self.iceberg_table_name}',
                retain_last => {self.num_keep_retention_snaps}
            )
        """

        _logger.info("\n Keeping %s latest snapshots\n", self.num_keep_retention_snaps)
        cursor.execute(expire_snapshot_sql)

    def call_remove_orphan_files(self, cursor):
        remove_orphan_files_sql = f"""
            CALL iceberg.system.remove_orphan_files (
                table => '{self.iceberg_db}.{self.iceberg_table_name}'
            )
        """
        _logger.info("\nRemoving orphan files\n")
        cursor.execute(remove_orphan_files_sql)

    def call_rewrite_manifests(self, cursor):
        rewrite_manifests_sql = f"""
            CALL iceberg.system.rewrite_manifests (
                table => '{self.iceberg_db}.{self.iceberg_table_name}'
            )
        """
        _logger.info("\nRewriting manifest files\n")
        cursor.execute(rewrite_manifests_sql)

    def create_stg_table(self, cursor):
        create_database_query_sql = f"""
            CREATE DATABASE IF NOT EXISTS {self.iceberg_db}
        """
        _logger.info("\nCreating database if not exists\n")
        cursor.execute(create_database_query_sql)

        _logger.info("\nCreating staging table\n")
        create_staging_table_sql = generate_create_table_sql(
            iceberg_db=self.iceberg_db,
            iceberg_table=self.iceberg_table_name,
            iceberg_columns_properties=self.table_properties,
            location=f"/staging/{self.iceberg_db}/{self.iceberg_table_name}/"
        )

        cursor.execute(create_staging_table_sql)

    def run_sql(self, cursor):
        with open(f"/opt/airflow/dags/{self.sql_path}", 'r') as file:
            sql_content = file.read()
        for sql in sql_content.split(';'):
            cursor.execute(sql)

    def execute(self, context):
        conn = self.get_spark_conn()
        cursor = conn.cursor()

        if self.sql_path == "":
            raise Exception("SQL content is empty, please modify your sql file!!!")
        else:
            self.create_stg_table(cursor)
            self.run_sql(cursor)

        if self.iceberg_db is None:
            _logger.warning("\niceberg_db param is None, clean iceberg table is skipped!!!\n")
        else:
            self.call_expire_snapshots(cursor)
            self.call_remove_orphan_files(cursor)
            self.call_rewrite_manifests(cursor)

        cursor.close()
        conn.close()

class IcebergOperatorPlugin(AirflowPlugin):
    name = "iceberg_operator_plugin"
    operators = [IcebergOperator]