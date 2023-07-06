from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import from_json, col, to_timestamp, window, expr, sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

from lib.logger import Log4j

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("Append Output and Tumbling Window Demo") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .config("spark.sql.shuffle.partitions", 2) \
        .getOrCreate()
    logger = Log4j(spark)
    booking_schema = StructType([
        StructField("bookingtime", StringType()),
        StructField("clientid", IntegerType()),
        StructField("clientname", StringType()),
        StructField("price", DoubleType())
   ])
    csv_df = spark.readStream \
            .schema(booking_schema) \
            .format("csv") \
            .option("path", "rebu") \
            .option("header", True) \
            .load()
    print(csv_df.isStreaming)
    results_df = csv_df.select("*")
    query = results_df.writeStream \
             .format("console") \
             .outputMode("append") \
             .start()
    query.awaitTermination()