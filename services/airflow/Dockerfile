FROM apache/airflow:2.7.3

USER root

# Install Java, SASL, and tools for PySpark + sasl builds
RUN apt-get update && \
    apt-get install -y \
        openjdk-11-jdk \
        gcc \
        g++ \
        build-essential \
        python3-dev \
        libkrb5-dev \
        libsasl2-dev \
        procps \
        psutils \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME so Spark works
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV YARN_CONF_DIR=/etc/hadoop

# Create Hadoop config directory
RUN mkdir -p /etc/hadoop

# Copy your Hadoop config files
COPY config/*.xml /etc/hadoop/

RUN mkdir -p /opt/airflow/jars/

COPY config/mysql-connector-java-8.0.21.jar /opt/airflow/jars

RUN ln -s /usr/lib/jvm/java-11-openjdk-arm64 /usr/lib/jvm/java-11-openjdk-amd64

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
