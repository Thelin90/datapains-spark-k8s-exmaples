import os
from typing import Type

from py4j.java_gateway import JavaObject
from pyspark.sql import SparkSession, DataFrame
from delta.tables import DeltaTable

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
    _df = _spark_session.createDataFrame(data, columns)

    # Only for demo
    _df.printSchema()

    return _df


def _flatten_schema(_df: DataFrame, denormalize_column="data") -> DataFrame:
    # Only for demo purpose
    _df.show()
    columns = ["id", "name", "surname", "age"]

    _df = _df.select("*", "data.*").drop("data")

    for old_col, new_col in zip(_df.columns, columns):
        _df = _df.withColumnRenamed(old_col, new_col)

    _df.printSchema()

    _df.show()

    return _df


def transform(_df: DataFrame) -> DataFrame:
    return _flatten_schema(_df=_df)


def load(_df: DataFrame, _spark_logger: Type[JavaObject], write_mode: str = "append"):
    _spark_logger.info(f"load data mode: {write_mode}")
    _df.write.format("delta").mode(write_mode).save(
        f"{os.getenv('SPARK_HOME')}/tables/people"
    )


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
    load(_df=df, _spark_logger=spark_logger)

    delta_table = DeltaTable.forPath(
        spark_session, f"{os.getenv('SPARK_HOME')}/tables/people"
    )

    delta_table.history().show()
