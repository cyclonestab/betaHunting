"""
OHLCV ETL Pipeline - Medallion Architecture

This pipeline has been restructured into medallion architecture layers:

📂 Bronze Layer (transformations/bronze/ohlcv_raw.py):
   - Ingests raw OHLCV data from source
   - Dataset: bronze_ohlcv_raw
   
📂 Silver Layer (transformations/silver/ohlcv_cleaned.py):
   - Cleans and transforms data
   - Unpivots wide format to long format
   - Calculates daily returns
   - Dataset: silver_ohlcv_cleaned

📂 Gold Layer (transformations/gold/ohlcv_aggregates.py):
   - Business-ready aggregations
   - Datasets: gold_ohlcv_monthly, gold_ohlcv_quarterly, gold_ohlcv_yearly

⚠️ Important: yfinance data fetch must happen outside the pipeline
   - Create a separate notebook/job to download yfinance data
   - Write results to a table or files
   - Update bronze layer to read from that location
"""
