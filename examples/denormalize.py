import os
from typing import Type

from py4j.java_gateway import JavaObject
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import StructType

SPARK_HOME_JARS = f"{os.getenv('SPARK_HOME')}/jars"
DELTA_VERSION = os.getenv("DELTA_VERSION")
SCALA_VERSION = os.getenv("SCALA_VERSION")


def get_session(app_name: str) -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()


def set_delta_python_jar(
    _spark_session: SparkSession, _spark_logger: Type[JavaObject]
) -> None:
    if SPARK_HOME_JARS and DELTA_VERSION and SCALA_VERSION:
        _spark_logger.info(
            f"SPARK HOME JARS: {SPARK_HOME_JARS}, \n"
            f"DELTA VERSION: {DELTA_VERSION}, \n"
            f"SCALA VERSION: {SCALA_VERSION}"
        )
        _spark_session.sparkContext.addPyFile(
            f"{SPARK_HOME_JARS}/delta-spark_{SCALA_VERSION}-{DELTA_VERSION}.jar"
        )


def get_spark_logger(_spark_session: SparkSession, log_level: str) -> Type[JavaObject]:
    _spark_session.sparkContext.setLogLevel(log_level)
    log4j = _spark_session._jvm.org.apache.log4j
    return log4j.LogManager.getLogger(__name__)


def extract(_spark_session: SparkSession) -> DataFrame:
    data = [
        [1, ("Alice", "Smith", 29)],
        [2, ("Bob", "Brown", 40)],
        [3, ("Charlie", "Johnson", 35)],
    ]
    columns = ["id", "data"]
    return _spark_session.createDataFrame(data, columns)


def _flatten_schema(_df: DataFrame, prefix="") -> DataFrame:
    fields = []

    for field in _df.schema.fields:
        field_name = f"{prefix}.{field.name}" if prefix else field.name
        if isinstance(field.dataType, StructType):
            nested_df = _df.select(col(col=field_name + ".*"))
            fields.extend(_flatten_schema(_df=nested_df, prefix=field_name).columns)
        else:
            fields.append(field_name)

    return _df.select(
        [col(col=field).alias(field.replace(__old=".", __new="_")) for field in fields]
    )


def transform(_df: DataFrame) -> DataFrame:
    return _flatten_schema(_df=_df)


def write(_df: DataFrame, _spark_logger: Type[JavaObject]):
    _spark_logger.info("Denormalized DataFrame:")
    _df.show()


if __name__ == "__main__":
    spark_session = get_session(app_name="test-example")
    spark_logger: Type[JavaObject] = get_spark_logger(
        _spark_session=spark_session,
        log_level="INFO",
    )
    spark_logger.info("Running spark in kubernetes with DataPains!")
    set_delta_python_jar(_spark_session=spark_session, _spark_logger=spark_logger)

    df: DataFrame = extract(_spark_session=spark_session)
    df: DataFrame = transform(_df=df)
    write(_df=df, _spark_logger=spark_logger)
