# datapains-spark-k8s-example

In this repo I show how to build a docker image running spark and pyspark, which will be compatible
with the official [spark operator](https://operatorhub.io/operator/spark-gcp).

Please also see my other [repository](https://github.com/Thelin90/datapains-spark-operator-k8s) where I show how to deploy the operator.

# Pre Requisites

* python3.9
* poetry `1.1.7`
* `docker-desktop`
* `make`

# Docker

```bash
make build-container-image
```

For `m1`
```bash
make build-container-image DOCKER_BUILD="buildx build --platform linux/amd64"
```

I have defined a `docker` image which uses:

* python [3.9](https://www.python.org/downloads/release/python-390/)
* spark version [4.0.0preview](https://mvnrepository.com/artifact/org.apache.spark/spark-core_2.13/3.5.1)
* delta version [4.0.0rc1](https://mvnrepository.com/artifact/io.delta/delta-spark_2.13/4.0.0rc1)
    * See official github release [here](https://github.com/delta-io/delta/releases/tag/v4.0.0rc1)
    * See official delta docs [here](https://docs.delta.io/4.0.0-preview/index.html)
* scala version [2.13](https://mvnrepository.com/artifact/org.scala-lang/scala-library/2.13.0)
* java version [17](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)

`NOTE!`
The `tools/scripts/entrypoint.sh` has been modified to setup `poetry` to use the docker images
poetry environment.

# Test locally

## Spark Shell

```bash
make local-pyspark-shell
```

* You will see how the `entrypoint` works in action
* The shell starts and you can play around with the spark distribution without having to set it up on your local machine, but rather run it in a shell in the docker image.

```bash
+ cd /opt/spark/work-dir
++ poetry show -v
++ cut -d ' ' -f 3
++ head -n1
+ export PYSPARK_PYTHON=/root/.cache/pypoetry/virtualenvs/datapains-spark-k8s-examples-2OPaUQvv-py3.9/bin/python
+ PYSPARK_PYTHON=/root/.cache/pypoetry/virtualenvs/datapains-spark-k8s-examples-2OPaUQvv-py3.9/bin/python
++ poetry show -v
++ head -n1
++ cut -d ' ' -f 3
+ export PYSPARK_DRIVER_PYTHON=/root/.cache/pypoetry/virtualenvs/datapains-spark-k8s-examples-2OPaUQvv-py3.9/bin/python
+ PYSPARK_DRIVER_PYTHON=/root/.cache/pypoetry/virtualenvs/datapains-spark-k8s-examples-2OPaUQvv-py3.9/bin/python
+ cd -
/
++ id -u
+ myuid=0
++ id -g
+ mygid=0
+ set +e
++ getent passwd 0
+ uidentry=root:x:0:0:root:/root:/bin/bash
+ set -e
+ '[' -z root:x:0:0:root:/root:/bin/bash ']'
+ SPARK_CLASSPATH=':opt/spark/jars/*'
+ env
+ grep SPARK_JAVA_OPT_
+ sort -t_ -k4 -n
+ sed 's/[^=]*=\(.*\)/\1/g'
+ readarray -t SPARK_EXECUTOR_JAVA_OPTS
+ '[' -n '' ']'
+ '[' -z x ']'
+ export PYSPARK_PYTHON
+ '[' -z x ']'
+ export PYSPARK_DRIVER_PYTHON
+ '[' -n '' ']'
+ '[' -z ']'
+ '[' -z ']'
+ '[' -z x ']'
+ SPARK_CLASSPATH='opt/spark/conf::opt/spark/jars/*'
+ case "$1" in
+ echo 'Non-spark-on-k8s command provided, proceeding in pass-through mode...'
Non-spark-on-k8s command provided, proceeding in pass-through mode...
+ CMD=("$@")
+ exec /usr/bin/tini -s -- pyspark --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/07/10 08:28:49 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.5.1
      /_/

Using Python version 3.9.2 (default, Feb 28 2021 17:03:44)
Spark context Web UI available at http://f6c40b7da839:4040
Spark context available as 'sc' (master = local[*], app id = local-1720600130530).
SparkSession available as 'spark'.
>>>
```

Quick example:
```bash
>>> from delta.tables import DeltaTable
>>> data = [[1, ("Alice", "Smith", 29)], [2, ("Bob", "Brown", 40)], [3, ("Charlie", "Johnson", 35)]]
>>> columns = columns = ["id", "data"]
>>> df = spark.createDataFrame(data, columns)
>>> 
```

# Deploy - Argo Workflow

Please go to my `argo workflow` [repo]() to see how I deploy an example job with this image, utilising
the spark operator with this base image which can be re-used.
