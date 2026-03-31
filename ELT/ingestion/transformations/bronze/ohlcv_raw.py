from pyspark import pipelines as dp
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, DateType

@dp.materialized_view(
    comment="Raw OHLCV data - Bronze layer with historical stock prices"
)
def bronze_ohlcv_raw():
    """
    Ingest raw OHLCV (Open, High, Low, Close, Volume) data.
    
    NOTE: This assumes yfinance data is pre-fetched and stored in one of:
    - A source table (e.g., workspace.default.yfinance_raw)
    - Files in a Volume or cloud storage (use Auto Loader)
    
    Current implementation reads from a source table.
    To use files instead, replace with Auto Loader pattern.
    """
    # Option 1: Read from existing table where yfinance data was loaded
    # Replace 'workspace.default.yfinance_raw' with your actual source
    source_df = spark.read.table("workspace.default.ticker")
    
    # Add ingestion metadata
    result = source_df.withColumn("ingestion_timestamp", F.current_timestamp())
    
    return result
