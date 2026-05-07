from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WordCount").getOrCreate()
text_file = spark.read.text("hdfs://path/to/file.txt")
counts = text_file.selectExpr("explode(split(value, ' ')) as word").groupBy("word").count()
counts.show()
