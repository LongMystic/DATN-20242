import requests
from .credentials import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    return requests.post(url, data=payload)

def notify_success(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['execution_date']
    send_telegram_message(f"✅ DAG <b>{dag_id}</b> - Task <b>{task_id}</b> succeeded at <i>{execution_date}</i>")

def notify_failure(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['execution_date']
    send_telegram_message(f"❌ DAG <b>{dag_id}</b> - Task <b>{task_id}</b> failed at <i>{execution_date}</i>")
