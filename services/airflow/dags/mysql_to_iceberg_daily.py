import pendulum
from airflow.models import DAG

from task_group.task_group import load_raw, load_staging, load_warehouse, clean_raw
from datetime import timedelta, datetime
from utils.utils import get_variables
from utils.constant import *

DAG_NAME = "mysql_to_iceberg_daily"

SCHEDULE_INTERVAL = "00 02 * * *"

default_args = {
    "owner": "airflow",
    "start_date": pendulum.today("UTC").add(days=-1),
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

variable = get_variables(DAG_NAME)

with DAG(
    dag_id=DAG_NAME,
    schedule_interval=SCHEDULE_INTERVAL,
    default_args=default_args,
    max_active_tasks=MAX_ACTIVE_TASKS,
    max_active_runs=MAX_ACTIVE_RUNS,
    tags=["daily", "longvk"]

) as dag:
    task_load_to_raw = load_raw(
        task_group_id="task_load_to_raw",
        **variable
    )

    task_load_to_staging = load_staging(
        task_group_id="task_load_to_staging",
        **variable
    )

    task_load_to_warehouse = load_warehouse(
        task_group_id="task_load_to_warehouse",
        **variable
    )

    task_clean_raw = clean_raw(
        task_group_id="task_clean_raw",
        **variable
    )

    (
        task_load_to_raw >> task_load_to_staging
        >> task_load_to_warehouse >> task_clean_raw
    )
