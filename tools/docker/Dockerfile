FROM openjdk:17-jdk-slim

RUN apt-get update && \
    apt-get -y install --no-install-recommends wget=1.21-1+deb11u1 --allow-downgrades && \
    apt-get -y install --no-install-recommends python3=3.9.2-3 --allow-downgrades && \
    apt-get -y install --no-install-recommends python3-pip=20.3.4-4+deb11u1 --allow-downgrades && \
    apt-get -y install --no-install-recommends python-is-python3=3.9.2-1 --allow-downgrades && \
    apt-get -y install --no-install-recommends python3-dev=3.9.2-3 --allow-downgrades && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

ENV SPARK_VERSION=3.5.1 \
    CORE_HADOOP_VERSION=3 \
    SPARK_HOME="opt/spark" \
    SPARK_URL="https://archive.apache.org/dist/spark"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN wget -q -O ${SPARK_HOME}-${SPARK_VERSION}-bin-hadoop${CORE_HADOOP_VERSION}.tgz \
    ${SPARK_URL}/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${CORE_HADOOP_VERSION}.tgz && \
    tar -xvzf ${SPARK_HOME}-${SPARK_VERSION}-bin-hadoop${CORE_HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${CORE_HADOOP_VERSION} ${SPARK_HOME} && \
    rm -rf ${SPARK_HOME}-${SPARK_VERSION}-bin-hadoop${CORE_HADOOP_VERSION}.tgz && \
    mv "${SPARK_HOME}/conf/spark-env.sh.template" "${SPARK_HOME}/conf/spark-env.sh"

COPY tools/docker/scripts/ /opt/
RUN chmod +x /opt/*.sh

ENV SCALA_VERSION=2.13 \
    MAVEN_URL="https://repo1.maven.org" \
    DELTA_VERSION="4.0.0rc1" \
    HADOOP_VERSION=3.3.4 \
    AWS_JAVA_SDK_VERSION=1.12.262 \
    GUAVA_VERSION=31.1 \
    GUAVA_DELETE_VERSION=14.0.1 \
    SPARK_SQL_VERSION=3.5.1 \
    FAILURE_ACCESS_VERSION=1.0.1 \
    WILDFLY_VERSION=1.0.7 \
    PROMETHEUS_VERSION=1.0.0

ENV PROMETHEUS_JAR_LOCATION="/prometheus/jmx_prometheus_javaagent-${PROMETHEUS_VERSION}.jar" \
    MAVEN_PROMETHEUS_JAVA_AGENT_URL="https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent"

####
# Baseline Jars such as Delta Spark, Hadoop AWS, Spark SQL, Prometheus etc
####
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN wget -q -O ${SPARK_HOME}/jars/delta-spark_${SCALA_VERSION}-${DELTA_VERSION}.jar \
    ${MAVEN_URL}/maven2/io/delta/delta-spark_${SCALA_VERSION}/${DELTA_VERSION}/delta-spark_${SCALA_VERSION}-${DELTA_VERSION}.jar && \
    wget -q -O ${SPARK_HOME}/jars/delta-storage-${DELTA_VERSION}.jar \
    ${MAVEN_URL}/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar && \
    wget -q -O ${SPARK_HOME}/jars/hadoop-aws-${HADOOP_VERSION}.jar \
    ${MAVEN_URL}/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar && \
    wget -q -O ${SPARK_HOME}/jars/hadoop-common-${HADOOP_VERSION}.jar \
    ${MAVEN_URL}/maven2/org/apache/hadoop/hadoop-common/${HADOOP_VERSION}/hadoop-common-${HADOOP_VERSION}.jar && \
    wget -q -O ${SPARK_HOME}/jars/aws-java-sdk-bundle-${AWS_JAVA_SDK_VERSION}.jar \
    ${MAVEN_URL}/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_JAVA_SDK_VERSION}/aws-java-sdk-bundle-${AWS_JAVA_SDK_VERSION}.jar && \
    wget -q -O ${SPARK_HOME}/jars/guava-${GUAVA_VERSION}-jre.jar \
    ${MAVEN_URL}/maven2/com/google/guava/guava/${GUAVA_VERSION}-jre/guava-${GUAVA_VERSION}-jre.jar && \
    wget -q -O ${SPARK_HOME}/jars/wildfly-openssl-${WILDFLY_VERSION}.Final.jar \
    ${MAVEN_URL}/maven2/org/wildfly/openssl/wildfly-openssl/${WILDFLY_VERSION}.Final/wildfly-openssl-${WILDFLY_VERSION}.Final.jar && \
    wget -q -O ${SPARK_HOME}/jars/spark-sql_${SCALA_VERSION}-${SPARK_SQL_VERSION}.jar \
    ${MAVEN_URL}/maven2/org/apache/spark/spark-sql_${SCALA_VERSION}/${SPARK_SQL_VERSION}/spark-sql_${SCALA_VERSION}-${SPARK_SQL_VERSION}.jar && \
    wget -q -O ${SPARK_HOME}/jars/failureaccess-${FAILURE_ACCESS_VERSION}.jar \
    ${MAVEN_URL}/maven2/com/google/guava/failureaccess/${FAILURE_ACCESS_VERSION}/failureaccess-${FAILURE_ACCESS_VERSION}.jar && \
    wget -q -O ${SPARK_HOME}/jars/jmx_prometheus_javaagent-${PROMETHEUS_VERSION}.jar \
    "${MAVEN_PROMETHEUS_JAVA_AGENT_URL}/${PROMETHEUS_VERSION}/jmx_prometheus_javaagent-${PROMETHEUS_VERSION}.jar" && \
    rm ${SPARK_HOME}/jars/guava-${GUAVA_DELETE_VERSION}.jar

ENV PY4J_VERSION=0.10.9.7 \
    PYTHONPATH="${SPARK_HOME}/python/:/opt/conda/bin/python"

ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-${PY4J_VERSION}-src.zip:$PYTHONPATH"

ENV PATH="$PATH:${SPARK_HOME}/bin:${SPARK_HOME}/python:${PATH}"

RUN apt-get update && \
    apt-get -y install --no-install-recommends gcc=4:10.2.1-1 --allow-downgrades && \
    apt-get -y install --no-install-recommends libc-bin=2.31-13+deb11u5 --allow-downgrades && \
    apt-get -y install --no-install-recommends libc6=2.31-13+deb11u5 --allow-downgrades && \
    apt-get -y install --no-install-recommends git=1:2.30.2-1+deb11u2 --allow-downgrades && \
    apt-get -y install --no-install-recommends make=4.3-4.1 --allow-downgrades && \
    apt-get -y install --no-install-recommends libgnutls30=3.7.1-5+deb11u3 --allow-downgrades && \
    apt-get -y install --no-install-recommends tini=0.19.0-1 --allow-downgrades && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

WORKDIR /opt/spark/work-dir

COPY examples /opt/spark/work-dir/examples/
COPY .git /opt/spark/work-dir/.git/
COPY [".pre-commit-config.yaml", "Makefile", "poetry.lock", "pyproject.toml", "/opt/spark/work-dir/"]

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONPATH="./:${PYTHONPATH}" \
    PIP_VERSION=24.1.1 \
    POETRY_VERSION=1.7.1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN python -m pip install --no-cache-dir pip=="${PIP_VERSION}" && \
    python -m pip install --no-cache-dir poetry=="${POETRY_VERSION}" && \
    poetry config virtualenvs.create true && \
    make setup-environment && \
    make info-environment

ENTRYPOINT ["/opt/entrypoint.sh"]
