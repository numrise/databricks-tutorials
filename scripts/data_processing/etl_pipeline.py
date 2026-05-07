#!/usr/bin/env python3
"""
ETL Pipeline Example
Extract, Transform, Load pattern
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, upper, lower, regexp_replace, 
    concat, lit, current_timestamp, year, month, day
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType


def create_sample_data(spark):
    """Create sample raw data"""
    schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("transaction_date", StringType(), True),
        StructField("product", StringType(), True)
    ])
    
    data = [
        (1, "john", "doe", "john@example.com", "555-1234", 100.50, "2024-01-15", "laptop"),
        (2, "jane", "smith", "jane@example.com", "555-5678", 250.75, "2024-01-16", "monitor"),
        (3, "bob", "johnson", "bob@example.com", None, 75.25, "2024-01-17", "keyboard"),
        (4, "alice", "williams", None, "555-9999", 150.00, "2024-01-18", "mouse"),
        (5, "charlie", "brown", "charlie@example.com", "555-3333", 500.00, "2024-01-19", "desk")
    ]
    
    return spark.createDataFrame(data, schema=schema)


def extract(spark):
    """E - Extract data from source"""
    print("🔵 EXTRACT: Loading raw data...")
    
    raw_df = create_sample_data(spark)
    print(f"   Rows loaded: {raw_df.count()}")
    
    return raw_df


def transform(df):
    """T - Transform/Clean data"""
    print("🟡 TRANSFORM: Cleaning and enriching data...")
    
    # Clean and standardize
    transformed = (df
        # Standardize names
        .withColumn("first_name", upper(col("first_name")))
        .withColumn("last_name", upper(col("last_name")))
        
        # Clean email
        .withColumn("email", lower(col("email")))
        
        # Clean phone (remove non-digits)
        .withColumn("phone", regexp_replace(col("phone"), "[^0-9]", ""))
        
        # Create full name
        .withColumn("full_name", 
                   concat(col("first_name"), lit(" "), col("last_name")))
        
        # Categorize amount
        .withColumn("amount_category",
                   when(col("amount") < 100, "Low")
                   .when(col("amount") < 300, "Medium")
                   .otherwise("High"))
        
        # Add processing metadata
        .withColumn("processed_at", current_timestamp())
        .withColumn("year", year(col("transaction_date")))
        .withColumn("month", month(col("transaction_date")))
        .withColumn("day", day(col("transaction_date")))
        
        # Select and reorder columns
        .select(
            "customer_id",
            "full_name",
            "first_name",
            "last_name",
            "email",
            "phone",
            "amount",
            "amount_category",
            "product",
            "transaction_date",
            "year",
            "month",
            "day",
            "processed_at"
        )
    )
    
    # Handle missing values
    transformed = transformed.na.fill({
        "email": "unknown@example.com",
        "phone": "0000000000"
    })
    
    print(f"   Rows transformed: {transformed.count()}")
    transformed.show(truncate=False)
    
    return transformed


def load(df, output_path):
    """L - Load data to destination"""
    print("🟢 LOAD: Writing data to destination...")
    
    # Write to CSV
    df.write.csv(
        f"{output_path}/csv",
        header=True,
        mode="overwrite"
    )
    
    # Write to Parquet (efficient columnar format)
    df.write.parquet(
        f"{output_path}/parquet",
        mode="overwrite"
    )
    
    # Write to JSON
    df.write.json(
        f"{output_path}/json",
        mode="overwrite"
    )
    
    print(f"   ✅ Data written to {output_path}/")


def main():
    # Initialize Spark
    spark = SparkSession.builder \
        .appName("ETLPipeline") \
        .master("local") \
        .getOrCreate()
    
    print("\n" + "=" * 60)
    print("ETL PIPELINE EXAMPLE")
    print("=" * 60 + "\n")
    
    # ETL Pipeline
    raw_data = extract(spark)
    print()
    
    transformed_data = transform(raw_data)
    print()
    
    load(transformed_data, "etl_output")
    
    print("\n" + "=" * 60)
    print("✅ ETL Pipeline Completed Successfully!")
    print("=" * 60 + "\n")
    
    # Display summary statistics
    print("SUMMARY STATISTICS:")
    print("-" * 60)
    transformed_data.groupBy("amount_category").count().show()
    transformed_data.groupBy("product").agg({"amount": "sum"}).show()
    
    spark.stop()


if __name__ == "__main__":
    main()
