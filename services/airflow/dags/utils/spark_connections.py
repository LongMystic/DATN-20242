from pyhive import hive
import json
from airflow.hooks.base import BaseHook


def get_spark_thrift_conn(hive_server2_conn_id: str = "hive_server2_default_id"):

    conn_params = BaseHook.get_connection(hive_server2_conn_id)

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