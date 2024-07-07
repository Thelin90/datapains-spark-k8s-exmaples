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
* spark version [3.5.1](https://mvnrepository.com/artifact/org.apache.spark/spark-core_2.13/3.5.1)
* delta version [4.0.0rc1](https://mvnrepository.com/artifact/io.delta/delta-spark_2.13/4.0.0rc1)
    * See official github release [here](https://github.com/delta-io/delta/releases/tag/v4.0.0rc1)
    * See official delta docs [here](https://docs.delta.io/4.0.0-preview/index.html)
* scala version [2.13](https://mvnrepository.com/artifact/org.scala-lang/scala-library/2.13.0)
* java version [17](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)

`NOTE!`
The `tools/scripts/entrypoint.sh` has been modified to setup `poetry` to use the docker images
poetry environment.

# Deploy - Argo Workflow

Please go to my `argo workflow` [repo]() to see how I deploy an example job with this image, utilising
the spark operator with this base image which can be re-used.
