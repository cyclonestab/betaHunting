from pyspark import pipelines as dp
from pyspark.sql import functions as F
from pyspark.sql.window import Window

@dp.materialized_view(
    comment="Cleaned OHLCV data - Silver layer with standardized format and quality checks"
)
@dp.expect_all({
    "valid_ticker": "ticker IS NOT NULL",
    "valid_date": "date IS NOT NULL",
    "valid_adj_close": "adj_close >= 0"
})
def silver_ohlcv_cleaned():
    """
    Transform raw OHLCV data into clean, standardized format.
    
    Transformations:
    - Unpivot wide format (tickers as columns) to long format (ticker as row)
    - Filter out null prices
    - Standardize date format
    - Add derived fields (day of week, month, quarter, year)
    - Calculate daily returns
    """
    bronze = spark.read.table("bronze_ohlcv_raw")
    
    # Get all column names except Date and metadata columns
    date_col = "Date" if "Date" in bronze.columns else "date"
    ticker_cols = [col for col in bronze.columns 
                   if col not in [date_col, "ingestion_timestamp"]]
    
    # Unpivot: convert from wide (tickers as columns) to long format
    # Stack creates (ticker, adj_close) pairs
    unpivoted = bronze.selectExpr(
        f"{date_col} as date",
        "ingestion_timestamp",
        f"stack({len(ticker_cols)}, {', '.join([f\"'{col}', `{col}`\" for col in ticker_cols])}) as (ticker, adj_close)"
    )
    
    # Filter out nulls and add derived date fields
    cleaned = unpivoted.filter(F.col("adj_close").isNotNull()) \
        .withColumn("year", F.year("date")) \
        .withColumn("quarter", F.quarter("date")) \
        .withColumn("month", F.month("date")) \
        .withColumn("day_of_week", F.dayofweek("date"))
    
    # Calculate daily returns (percentage change from previous day)
    window_spec = Window.partitionBy("ticker").orderBy("date")
    result = cleaned.withColumn(
        "daily_return_pct",
        ((F.col("adj_close") - F.lag("adj_close").over(window_spec)) / F.lag("adj_close").over(window_spec)) * 100
    )
    
    return result
