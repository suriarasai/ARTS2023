from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
lines = spark.read.text("Singapore.txt")
print(lines.count())
#wordCounts = lines.select(explode(split(lines.value, "\s+")).alias("word")).groupBy("word").count()
#print(wordCounts.collect())