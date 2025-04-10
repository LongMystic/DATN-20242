# Define base image
FROM apache/superset:latest

# Switching to root to install the required packages
USER root

# Intall required dependencies.
# Example: installing the MySQL driver to connect to the metadata database
# if you prefer Postgres, you may want to use `psycopg2-binary` instead
RUN pip install pyhive thrift thrift-sasl

# Define additional environment variables to be used
ENV ADMIN_EMAIL=admin@superset.com ADMIN_USERNAME=admin ADMIN_PASSWORD=admin

# Add custom superset_config.py file and shell files
COPY ./conf/superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py
#define variable that is used by Superset to look for config python file.

COPY superset-init.sh /app/superset-custom.sh
RUN chmod +x /app/superset-custom.sh

# Switching back to using the `superset` user
USER superset
ENTRYPOINT [ "/app/superset-custom.sh" ]