from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

from lib.logger import Log4j

spark = SparkSession \
    .builder \
    .appName("Booking File Streaming Demo") \
    .master("local[*]") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .config("spark.sql.streaming.schemaInference", "true") \
    .getOrCreate()

logger = Log4j(spark)

print("start")
raw_df = spark.readStream \
    .format("json") \
    .option("path", "rebu-booking") \
    .option("maxFilesPerTrigger", 1) \
    .load()
print("0")
raw_df.printSchema()
print("1")
named_df = raw_df.selectExpr("BookingID", "MessageSubmittedTime", "MessageReceivedTime", "CustomerID",
                             "CustomerName", "PhoneNumber", "PickUpLocation", "PickupPostcode",
                             "PickUpTime", "DropLocation", "DropPostcode",
                             "TaxiType", "FareType", "Fare")
print("2")
named_df.printSchema()
print("3")
bookingWriterQuery = named_df.writeStream \
    .format("json") \
    .queryName("Flattened Booking Writer") \
    .outputMode("append") \
    .option("path", "rebu-output") \
    .option("checkpointLocation", "rebu-chk-point-dir") \
    .trigger(processingTime="1 minute") \
    .start()

print("Flattened Taxi Booking Writer started")
bookingWriterQuery.awaitTermination()