# Use the official Apache Airflow image as a base
FROM apache/airflow:2.6.1

# Switch to root user to install additional packages
USER root

# Install Java (required for PySpark)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

USER airflow

# Install PySpark
RUN pip install pyspark
