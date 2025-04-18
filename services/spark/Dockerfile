FROM apache/spark:3.3.3-python3

USER root
# Create spark_user with UID 1000
RUN useradd -u 1000 -ms /bin/bash spark_user

# Optional: give ownership of Spark folder
RUN chown -R spark_user:spark_user /opt/spark

# Set the default user
USER spark_user