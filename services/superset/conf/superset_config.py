# superset_config/superset_config.py
import os

# Superset specific config
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = 8088

# Flask App Builder configuration
APP_NAME = "Lakehouse Analytics"
SECRET_KEY = 'longvk@123'


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