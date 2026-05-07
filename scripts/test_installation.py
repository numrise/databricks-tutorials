#!/usr/bin/env python3
"""
Test Spark Installation
Verify that Spark is correctly installed and configured
"""

import sys
import subprocess


def check_java():
    """Check Java installation"""
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        version_line = result.stderr.split('\n')[0]
        print(f"✅ Java: {version_line}")
        return True
    except FileNotFoundError:
        print("❌ Java: Not found")
        return False


def check_spark():
    """Check Spark installation"""
    try:
        result = subprocess.run(["spark-submit", "--version"], capture_output=True, text=True)
        print(f"✅ Spark: {result.stderr.strip().split(chr(10))[0]}")
        return True
    except FileNotFoundError:
        print("❌ Spark: Not found")
        return False


def check_python():
    """Check Python and PySpark"""
    print(f"✅ Python: {sys.version.split()[0]}")
    
    try:
        import pyspark
        print(f"✅ PySpark: {pyspark.__version__}")
        return True
    except ImportError:
        print("❌ PySpark: Not installed")
        return False


def test_spark_session():
    """Test creating SparkSession"""
    try:
        from pyspark.sql import SparkSession
        
        spark = SparkSession.builder \
            .appName("InstallationTest") \
            .master("local[1]") \
            .getOrCreate()
        
        # Test basic operation
        df = spark.range(10)
        result = df.count()
        
        spark.stop()
        
        print(f"✅ SparkSession: Created successfully (tested with 10 rows)")
        return True
    except Exception as e:
        print(f"❌ SparkSession: {str(e)}")
        return False


def main():
    print("\n" + "=" * 50)
    print("SPARK INSTALLATION TEST")
    print("=" * 50 + "\n")
    
    checks = [
        check_java(),
        check_python(),
        check_spark(),
        test_spark_session()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("✅ ALL TESTS PASSED - Spark is ready to use!")
    else:
        print("❌ SOME TESTS FAILED - Check installation")
        sys.exit(1)
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
