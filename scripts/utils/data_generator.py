#!/usr/bin/env python3
"""
Data Generator Utility
Generate sample datasets for testing
"""

import random
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, 
    DoubleType, TimestampType
)


class DataGenerator:
    """Generate sample datasets"""
    
    def __init__(self, spark):
        self.spark = spark
        self.first_names = [
            "Alice", "Bob", "Charlie", "David", "Eve",
            "Frank", "Grace", "Henry", "Iris", "Jack"
        ]
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones",
            "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"
        ]
        self.departments = ["Engineering", "Sales", "Marketing", "HR", "Finance"]
        self.products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"]
    
    def generate_employees(self, num_rows=100):
        """Generate sample employee data"""
        data = []
        for i in range(1, num_rows + 1):
            data.append((
                i,
                random.choice(self.first_names),
                random.choice(self.last_names),
                random.choice(self.departments),
                random.randint(50000, 150000),  # salary
                random.randint(22, 65)  # age
            ))
        
        schema = StructType([
            StructField("emp_id", IntegerType()),
            StructField("first_name", StringType()),
            StructField("last_name", StringType()),
            StructField("department", StringType()),
            StructField("salary", IntegerType()),
            StructField("age", IntegerType())
        ])
        
        return self.spark.createDataFrame(data, schema=schema)
    
    def generate_sales(self, num_rows=500):
        """Generate sample sales data"""
        data = []
        base_date = datetime(2024, 1, 1)
        
        for i in range(num_rows):
            data.append((
                i + 1,
                random.randint(1, 100),  # emp_id
                random.choice(self.products),
                random.uniform(10, 1000),  # amount
                base_date + timedelta(days=random.randint(0, 90))
            ))
        
        schema = StructType([
            StructField("transaction_id", IntegerType()),
            StructField("emp_id", IntegerType()),
            StructField("product", StringType()),
            StructField("amount", DoubleType()),
            StructField("sale_date", TimestampType())
        ])
        
        return self.spark.createDataFrame(data, schema=schema)
    
    def generate_logs(self, num_rows=1000):
        """Generate sample log data"""
        levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        messages = [
            "User login successful",
            "Database connection failed",
            "Memory usage exceeded threshold",
            "Request completed",
            "Timeout occurred"
        ]
        
        data = []
        base_date = datetime.now()
        
        for i in range(num_rows):
            data.append((
                i + 1,
                random.choice(levels),
                random.choice(messages),
                base_date - timedelta(hours=random.randint(0, 72))
            ))
        
        schema = StructType([
            StructField("log_id", IntegerType()),
            StructField("level", StringType()),
            StructField("message", StringType()),
            StructField("timestamp", TimestampType())
        ])
        
        return self.spark.createDataFrame(data, schema=schema)


def main():
    spark = SparkSession.builder \
        .appName("DataGenerator") \
        .master("local") \
        .getOrCreate()
    
    gen = DataGenerator(spark)
    
    print("Generating sample datasets...\n")
    
    # Generate employees
    print("📊 Employee Data:")
    employees = gen.generate_employees(20)
    employees.show(10)
    
    # Generate sales
    print("\n📊 Sales Data:")
    sales = gen.generate_sales(50)
    sales.show(10)
    
    # Generate logs
    print("\n📊 Log Data:")
    logs = gen.generate_logs(50)
    logs.show(10)
    
    # Save to files
    print("\nSaving datasets...")
    employees.write.csv("sample_data/employees", header=True, mode="overwrite")
    sales.write.csv("sample_data/sales", header=True, mode="overwrite")
    logs.write.csv("sample_data/logs", header=True, mode="overwrite")
    
    print("✅ Datasets saved to sample_data/")
    
    spark.stop()


if __name__ == "__main__":
    main()
