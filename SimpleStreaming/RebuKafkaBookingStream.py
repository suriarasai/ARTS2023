from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

from lib.logger import Log4j

spark = SparkSession \
    .builder \
    .appName("Booking Kafka Streaming Demo") \
    .master("local[*]") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .config("spark.sql.streaming.schemaInference", "true") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1") \
    .getOrCreate()

logger = Log4j(spark)

print("start")
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "bookings") \
    .option("startingOffsets", "earliest") \
    .load()

print("0")
kafka_df.printSchema()
print("1")
bookingWriterQuery = kafka_df.writeStream \
    .format("json") \
    .queryName("Flattened Booking Writer") \
    .outputMode("append") \
    .option("path", "rebu-output") \
    .option("checkpointLocation", "rebu-chk-point-dir") \
    .trigger(processingTime="1 minute") \
    .start()

print("Flattened Taxi Booking Writer started")
bookingWriterQuery.awaitTermination()