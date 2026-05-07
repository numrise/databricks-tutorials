#!/bin/bash
# Spark Setup Script
# Downloads and configures Apache Spark for local development

set -e

echo "======================================"
echo "Apache Spark Setup Script"
echo "======================================"

SPARK_VERSION="3.5.0"
HADOOP_VERSION="3"
INSTALL_DIR="$HOME"

echo ""
echo "📦 Downloading Spark $SPARK_VERSION..."
cd /tmp
wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

echo "📂 Extracting..."
tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

echo "📍 Installing to $INSTALL_DIR/spark-${SPARK_VERSION}..."
mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $INSTALL_DIR/spark-${SPARK_VERSION}

echo "🔧 Configuring environment..."

# Add to bashrc/zshrc
SHELL_RC="$HOME/.bashrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

# Backup original
cp "$SHELL_RC" "$SHELL_RC.backup"

# Add Spark environment variables
cat >> "$SHELL_RC" << 'EOF'

# Spark Configuration
export SPARK_HOME=$HOME/spark-3.5.0
export PATH=$SPARK_HOME/bin:$PATH
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYSPARK_PYTHON=python3
export PYSPARK_DRIVER_PYTHON=python3
EOF

echo ""
echo "✅ Installation Complete!"
echo ""
echo "Next steps:"
echo "1. Reload shell: source $SHELL_RC"
echo "2. Verify: spark-submit --version"
echo "3. Start: pyspark"
echo ""
echo "Spark installed at: $INSTALL_DIR/spark-${SPARK_VERSION}"
