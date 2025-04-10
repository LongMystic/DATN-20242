from airflow.models import Variable
from typing import Any, Dict

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