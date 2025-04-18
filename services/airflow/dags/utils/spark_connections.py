from pyhive import hive
import json
from airflow.hooks.base import BaseHook
from pyspark.sql import SparkSession

def get_spark_thrift_conn(spark_conn_id: str = "spark_conn_id"):

    conn_params = BaseHook.get_connection(spark_conn_id)

    extra = json.loads(conn_params.extra or {})
    password = conn_params.password if conn_params.login else None
    conn = hive.connect(
        host=conn_params.host,
        port=conn_params.port,
        username=conn_params.login,
        password=password,
        database=conn_params.schema,
        auth=extra.get("auth", "NOSASL")
    )
    print("NOTICE: Please close conn after using or use with () statement for auto-closing!")
    return conn



def get_spark_session(app_name="AirflowApp", master="yarn"):
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.proxy.user", "spark_user")
        .config("spark.yarn.resourcemanager.hostname", "resourcemanager")
        .config("spark.jars", "/opt/airflow/jars/mysql-connector-java-8.0.21.jar")
        .config("spark.executor.memory", "1g")
        .config("spark.executor.cores", "1")
        .config("spark.executor.instances", "2")
        # Optional: metrics for Prometheus if needed
        .config("spark.ui.prometheus.enabled", "true")
        .getOrCreate()
    )

    return spark