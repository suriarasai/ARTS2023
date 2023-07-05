from pyspark.sql import SparkSession

from lib.logger import Log4j


spark = SparkSession.builder.appName("SparkSQL").getOrCreate()
logger = Log4j(spark)
spark.sparkContext.setLogLevel("ERROR")
surveyDF = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("data/sample.csv")

surveyDF.createOrReplaceTempView("survey_tbl")
countDF = spark.sql("select Country, count(1) as count from survey_tbl where Age<40 group by Country")
countDF.show()