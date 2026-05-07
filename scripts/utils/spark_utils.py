#!/usr/bin/env python3
"""
Spark Utilities
Common helper functions for Spark operations
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SparkUtils:
    """Common Spark utilities"""
    
    @staticmethod
    def get_session(app_name="SparkApp", master="local"):
        """Create or get SparkSession"""
        return SparkSession.builder \
            .appName(app_name) \
            .master(master) \
            .getOrCreate()
    
    @staticmethod
    def create_sample_data(spark):
        """Create sample employee data"""
        data = [
            (1, "Alice", "Engineering", 85000),
            (2, "Bob", "Sales", 72000),
            (3, "Charlie", "Engineering", 78000),
            (4, "David", "Management", 95000),
            (5, "Eve", "Sales", 68000)
        ]
        return spark.createDataFrame(data, ["id", "name", "dept", "salary"])
    
    @staticmethod
    def add_salary_grade(df):
        """Add salary grade column"""
        return df.withColumn("grade",
            when(col("salary") < 70000, "C")
            .when(col("salary") < 85000, "B")
            .otherwise("A")
        )
    
    @staticmethod
    def get_data_quality_report(df):
        """Generate data quality report"""
        report = {
            "total_rows": df.count(),
            "total_columns": len(df.columns),
            "columns": df.columns,
            "dtypes": dict(df.dtypes),
            "null_counts": {col: df.filter(df[col].isNull()).count() 
                          for col in df.columns}
        }
        return report
    
    @staticmethod
    def display_report(report):
        """Display quality report"""
        print("\n" + "=" * 60)
        print("DATA QUALITY REPORT")
        print("=" * 60)
        print(f"Total Rows: {report['total_rows']}")
        print(f"Total Columns: {report['total_columns']}")
        print(f"Columns: {', '.join(report['columns'])}")
        print(f"\nData Types:")
        for col, dtype in report['dtypes'].items():
            print(f"  {col:20} -> {dtype}")
        print(f"\nNull Counts:")
        for col, count in report['null_counts'].items():
            percentage = (count / report['total_rows'] * 100) if report['total_rows'] > 0 else 0
            print(f"  {col:20} -> {count:5} ({percentage:5.1f}%)")
        print("=" * 60 + "\n")


def main():
    """Example usage"""
    # Create session
    spark = SparkUtils.get_session("UtilitiesDemo")
    
    # Create sample data
    df = SparkUtils.create_sample_data(spark)
    print("Original Data:")
    df.show()
    
    # Add salary grade
    df_with_grade = SparkUtils.add_salary_grade(df)
    print("\nWith Salary Grade:")
    df_with_grade.show()
    
    # Get quality report
    report = SparkUtils.get_data_quality_report(df)
    SparkUtils.display_report(report)
    
    spark.stop()


if __name__ == "__main__":
    main()
