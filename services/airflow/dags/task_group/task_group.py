import logging

from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from mysql_to_hdfs_operator import MySQLToHDFSOperator
from airflow.operators.empty import EmptyOperator
# from plugins.iceberg_operator import IcebergOperator
from utils.utils import get_variables
DAG_NAME = "mysql_to_iceberg_daily"
variable = get_variables(DAG_NAME)

def load_raw(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        mysql_conn_id = kwargs.get("mysql_conn_id")
        spark_conn_id = kwargs.get("spark_conn_id")
        hdfs_conn_id = kwargs.get("hdfs_conn_id")

        task_load_raw = MySQLToHDFSOperator(
            task_id = f"load_table_to_raw",
            schema="test",
            sql="SELECT * FROM test.category",
            **kwargs
        )
        
        task_load_raw

        # task = PythonOperator(
        #     task_id="python",
        #     python_callable=python_callable
        # )
        # task
    return task_group


def python_callable():
    logging.info(variable)

def load_staging(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        empty = EmptyOperator(task_id="empty")
        empty
        return task_group


def load_warehouse(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        empty = EmptyOperator(task_id="empty")
        empty
        return task_group


def clean_raw(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        empty = EmptyOperator(task_id="empty")
        empty
        return task_group