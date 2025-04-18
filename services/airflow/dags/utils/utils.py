from airflow.models import Variable
from typing import Any, Dict

from schema.Table import Table


def get_variables(
        name,
        deserialize_json=True,
        default_var={}
) -> Dict[str, Any]:
    variables = Variable.get(
        key=name,
        deserialize_json=deserialize_json,
        default_var=default_var
    )
    return variables

def generate_create_table_sql(iceberg_db, iceberg_table, iceberg_columns_properties, location):
    with open("/opt/airflow/dags/sql/common/create_table_template.sql", 'r') as sql_file:
        template = sql_file.read()
    sql = template.format(
        iceberg_db=iceberg_db,
        iceberg_table=iceberg_table,
        iceberg_columns_properties=iceberg_columns_properties,
        location=f"'hdfs://namenode:8020{location}'"
    )
    return sql


def generate_table_properties_sql(table: Table) -> str:
    table_columns = table.COLUMNS
    table_properties = ""
    for column in table_columns:
        column_name = column['name']
        column_type = column['type']
        column_comment = column['comment']
        if column_comment:
            table_properties += f"{column_name} {column_type} COMMENT '{column_comment}',\n"
        else:
            table_properties += f"{column_name} {column_type},\n"
    # remove the last comma and newline
    table_properties = table_properties.rstrip(",\n")
    return table_properties