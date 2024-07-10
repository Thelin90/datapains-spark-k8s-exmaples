from typing import Type

from py4j.java_gateway import JavaObject
from pyspark.sql import SparkSession, DataFrame

#################
# Only for demo #
#################


def get_session(app_name: str) -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()


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

    _df.printSchema()

    return _df


def _flatten_schema(_df: DataFrame, denormalize_column="data") -> DataFrame:
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
    _df.show()


if __name__ == "__main__":
    spark_session = get_session(app_name="test-example")
    spark_logger: Type[JavaObject] = get_spark_logger(
        _spark_session=spark_session,
        log_level="INFO",
    )
    spark_logger.info("Running spark in kubernetes with DataPains!")

    df: DataFrame = extract(_spark_session=spark_session)
    df: DataFrame = transform(_df=df)
    load(_df=df, _spark_logger=spark_logger)
