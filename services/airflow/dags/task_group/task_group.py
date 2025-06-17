import logging
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator

from mysql_to_hdfs_operator import MySQLToHDFSOperator
from mysql_to_hdfs_operator_v2 import MySQLToHDFSOperatorV2
from mysql_to_hdfs_operator_v3 import MySQLToHDFSOperatorV3
from hdfs_to_iceberg_operator import HDFSToIcebergOperator
from iceberg_operator import IcebergOperator

from schema.schema_raw import ALL_TABLES as ALL_TABLES_RAW
from schema.schema_staging import ALL_TABLES as ALL_TABLES_STG
from schema.schema_business import ALL_TABLES as ALL_TABLES_BUSINESS
from utils.utils import get_variables, generate_table_properties_sql
DAG_NAME = "mysql_to_iceberg_daily"
variable = get_variables(DAG_NAME)

def load_raw(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        spark_conn_id = kwargs.get("spark_conn_id")
        mysql_conn_id = kwargs.get("mysql_conn_id")
        business_date = datetime.strptime(kwargs.get("business_date"), '%Y-%m-%d').date()

        partition_column = "id"

        start_date = datetime.strptime('2013-01-01', '%Y-%m-%d').date()

        d = (datetime.now().date() - business_date).days % 5
        from_date = start_date + relativedelta(years=d)
        to_date = start_date + relativedelta(years=d+1)

        params = {}
        for tbl in ALL_TABLES_RAW:
            tbl_name = tbl.table_name
            if tbl_name == "sales":
                params = { 
                    # "from_date": from_date.strftime("'%Y-%m-%d'"),  # Add quotes for SQL
                    # "to_date": to_date.strftime("'%Y-%m-%d'")  # Add quotes for SQL
                }
            
            
            task_load_raw = MySQLToHDFSOperatorV3(
                task_id = f"load_table_{tbl_name}_to_raw_layer",
                mysql_conn_id=mysql_conn_id,
                spark_conn_id=spark_conn_id,
                hdfs_path=f"/raw/{tbl_name}_tmp/{datetime.now().strftime('%Y-%m-%d')}",
                schema="test",
                params = params,
                table=tbl_name,
                sql=tbl.SQL,
                partition_column=partition_column,
                trigger_rule='all_done'
            )
            task_load_raw

    return task_group

def load_staging(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        spark_conn_id = kwargs.get("spark_conn_id")

        for tbl in ALL_TABLES_RAW:
            tbl_name = tbl.table_name
            task_load_staging = HDFSToIcebergOperator(
                task_id=f"load_table_{tbl_name}_to_staging_layer",
                iceberg_table_name=tbl_name,
                num_keep_retention_snaps=2,
                iceberg_db="sales_staging",
                spark_conn_id=spark_conn_id,
                table_properties=generate_table_properties_sql(tbl),
                trigger_rule='all_done'
            )
            task_load_staging
    return task_group


def load_warehouse(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        spark_conn_id = kwargs.get("spark_conn_id")
        for tbl in ALL_TABLES_STG:
            tbl_name = tbl.table_name
            task_load_warehouse = IcebergOperator(
                task_id=f"load_table_{tbl_name}_to_business_layer",
                spark_conn_id=spark_conn_id,
                sql_path=tbl.SQL,
                iceberg_table_name=tbl.table_name,
                num_keep_retention_snaps=2,
                iceberg_db="sales_business",
                iceberg_db_stg="sales_staging",
                table_properties=generate_table_properties_sql(tbl),
                trigger_rule='all_done'
            )
            task_load_warehouse
        return task_group
    

def load_agg_warehouse(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        spark_conn_id = kwargs.get("spark_conn_id")
        for tbl in ALL_TABLES_BUSINESS:
            tbl_name = tbl.table_name
            task_load_agg_warehouse = IcebergOperator(
                task_id=f"load_table_{tbl_name}_to_business_layer",
                spark_conn_id=spark_conn_id,
                sql_path=tbl.SQL,
                iceberg_table_name=tbl.table_name,
                iceberg_db="sales_business",
                table_properties=generate_table_properties_sql(tbl),
                trigger_rule='all_done'
            )
            task_load_agg_warehouse
        return task_group

def clean_raw(task_group_id, **kwargs):
    with TaskGroup(task_group_id) as task_group:
        spark_conn_id = kwargs.get("spark_conn_id")
        for tbl in ALL_TABLES_RAW:
            tbl_name = tbl.table_name
            task_clean_raw = IcebergOperator(
                task_id=f"clean_table_{tbl_name}_from_raw_layer",
                spark_conn_id=spark_conn_id,
                sql_path=tbl.SQL,
                iceberg_table_name=tbl.table_name,
                iceberg_db="sales_staging",
                trigger_rule='all_done'
            )
            task_clean_raw
        return task_group
    

