# superset_config/superset_config.py
import os

# Superset specific config
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = 8088

# Flask App Builder configuration
APP_NAME = "Lakehouse Analytics"
SECRET_KEY = 'longvk@123'

# # Database configuration
# SQLALCHEMY_DATABASE_URI = 'sqlite:////app/superset.db'
ENABLE_PROXY_FIX = True
# Enable feature flags
FEATURE_FLAGS = {
    "ENABLE_JAVASCRIPT_CONTROLS": True,
    "DASHBOARD_CACHE": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "ALERT_REPORTS": True,
    "DASHBOARD_RBAC": True
}

# # Hive/Spark SQL connection
# SQLALCHEMY_CUSTOM_PASSWORD_STORE = {}
#
# # Add Hive/Spark SQL connection
# def get_hive_connection():
#     return {
#         'sqlalchemy_uri': 'hive://hive@spark-thriftserver:10000/default',
#         'extra': '{"engine_params": {"connect_args": {"auth": "NOSASL"}}}',
#     }
#
# SQLALCHEMY_CUSTOM_PASSWORD_STORE['hive_connection'] = get_hive_connection