#!/usr/bin/env python3
"""
Improved Word Count Example
Classic MapReduce pattern in Spark
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col, count
import sys


def word_count_rdd(spark, text_file_path):
    """Word count using RDD API"""
    print("=" * 50)
    print("Word Count - RDD Approach")
    print("=" * 50)
    
    sc = spark.sparkContext
    text_rdd = sc.textFile(text_file_path)
    
    # Split, clean, and count
    counts = (text_rdd
        .flatMap(lambda line: line.split())
        .map(lambda word: word.lower())
        .map(lambda word: word.replace(".", "").replace(",", ""))
        .filter(lambda word: len(word) > 0)
        .map(lambda word: (word, 1))
        .reduceByKey(lambda a, b: a + b)
        .sortBy(lambda x: x[1], ascending=False)
    )
    
    return counts.collect()


def word_count_dataframe(spark, text_file_path):
    """Word count using DataFrame API"""
    print("\n" + "=" * 50)
    print("Word Count - DataFrame Approach")
    print("=" * 50)
    
    # Read file
    df = spark.read.text(text_file_path)
    
    # Process
    word_counts = (df
        .select(explode(split(lower(col("value")), " ")).alias("word"))
        .filter(col("word") != "")
        .groupBy("word")
        .count()
        .orderBy(col("count").desc())
    )
    
    return word_counts.collect()


def create_sample_file():
    """Create sample text file for testing"""
    sample_text = """
    Apache Spark is a fast and general-purpose cluster computing system
    Spark provides high-level APIs in Scala, Java, Python, and R
    Spark runs on Hadoop, Mesos, standalone, or in the cloud
    Spark can access diverse data sources including HDFS, HBase, and S3
    Spark is Lightning-fast cluster computing
    """
    
    with open("sample.txt", "w") as f:
        f.write(sample_text)
    
    return "sample.txt"


def main():
    # Create SparkSession
    spark = SparkSession.builder \
        .appName("WordCountExample") \
        .master("local") \
        .getOrCreate()
    
    # Create or use sample file
    if len(sys.argv) > 1:
        text_file = sys.argv[1]
    else:
        print("Creating sample file...")
        text_file = create_sample_file()
    
    # RDD approach
    rdd_results = word_count_rdd(spark, text_file)
    print("\nTop 10 words (RDD approach):")
    for word, count in rdd_results[:10]:
        print(f"  {word:15} -> {count:5}")
    
    # DataFrame approach
    df_results = word_count_dataframe(spark, text_file)
    print("\nTop 10 words (DataFrame approach):")
    df_results.show(10, truncate=False)
    
    # Save results
    print("\nSaving results to CSV...")
    df_results.write.csv("word_counts", header=True, mode="overwrite")
    print("✅ Results saved to word_counts/")
    
    spark.stop()


if __name__ == "__main__":
    main()
