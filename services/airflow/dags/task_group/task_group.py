import logging

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator

from mysql_to_hdfs_operator import MySQLToHDFSOperator
from mysql_to_hdfs_operator_v2 import MySQLToHDFSOperatorV2
from mysql_to_hdfs_operator_v3 import MySQLToHDFSOperatorV3
from hdfs_to_iceberg_operator import HDFSToIcebergOperator
from iceberg_operator import IcebergOperator

from schema.sales.schema_raw import ALL_TABLES as ALL_TABLES_RAW
from schema.sales.schema_staging import ALL_TABLES as ALL_TABLES_STG

from utils.utils import get_variables, generate_table_properties_sql
DAG_NAME = "mysql_to_iceberg_daily"
variable = get_variables(DAG_NAME)

def load_raw(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        spark_conn_id = kwargs.get("spark_conn_id")
        mysql_conn_id = kwargs.get("mysql_conn_id")
        
        task_load_raw = MySQLToHDFSOperatorV3(
            task_id = f"load_table_to_raw_layer",
            mysql_conn_id=mysql_conn_id,
            spark_conn_id=spark_conn_id,
            hdfs_path="/raw/category_tmp",
            schema="test",
            table="category",
            sql=""
        )
        task_load_raw

    return task_group

def load_staging(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        spark_conn_id = kwargs.get("spark_conn_id")

        for tbl in ALL_TABLES_RAW:
            tbl_name = tbl.table_name
            task_load_staging = HDFSToIcebergOperator(
                task_id=f"load_table_to_staging_layer",
                iceberg_table_name=tbl_name,
                num_keep_retention_snaps=5,
                iceberg_db="longvk_test",
                spark_conn_id=spark_conn_id,
                table_properties=generate_table_properties_sql(tbl)
            )
            task_load_staging
    return task_group


def load_warehouse(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        spark_conn_id = kwargs.get("spark_conn_id")
        for tbl in ALL_TABLES_STG:
            task_load_warehouse = IcebergOperator(
                task_id=f"load_table_to_business_layer",
                spark_conn_id=spark_conn_id,
                sql_path=tbl.SQL,
                iceberg_table_name=tbl.table_name,
                num_keep_retention_snaps=5,
                iceberg_db="longvk_test",
                table_properties=generate_table_properties_sql(tbl)
            )
            task_load_warehouse
        return task_group