CREATE OR REPLACE MATERIALIZED VIEW ticker AS
    SELECT explode(
        array(
          "AAPL", "AMD", "AMZN", "ARM", "ASML", "AVGO", "AXP", "BAC",
          "BRK-B", "C", "COIN", "COST", "GOOG", "GS", "HD", "HSBC", "IBKR",
          "IBM", "INTC", "JNJ", "JPM", "KO", "LIN", "LLY", "MA", "MCD",
          "META", "MRK", "MS", "MSFT", "NFLX", "NVDA", "PEP", "PG", "QCOM",
          "SCHW", "TSLA", "TSM", "TMO", "UNH", "V", "WFC", "WMT", "QQQ", "ONEQ",
          "XLF", "SMH", "VTI", "VT", "SPY", "DIA", "OEF", "IWM", "JEPI", "JEPQ", "SCHD",
          "SCHG", "000001.SS", "2888.HK", "^HSI", "GLD", "IBIT", "BTC-USD"
        )
    ) AS ticker;