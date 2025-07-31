import pandas_ta as ta

def add_rsi(df, length=14):
    """
    Calculates the Relative Strength Index (RSI) and adds it to the DataFrame.
    :param df: pandas DataFrame with 'close' prices.
    :param length: The time period for RSI calculation.
    """
    df.ta.rsi(length=length, append=True)
    return df

def add_macd(df, fast=12, slow=26, signal=9):
    """
    Calculates the Moving Average Convergence Divergence (MACD) and adds it to the DataFrame.
    :param df: pandas DataFrame with 'close' prices.
    :param fast: The fast period for the MACD.
    :param slow: The slow period for the MACD.
    :param signal: The signal period for the MACD.
    """
    df.ta.macd(fast=fast, slow=slow, signal=signal, append=True)
    return df

def add_bollinger_bands(df, length=20, std=2):
    """
    Calculates Bollinger Bands and adds them to the DataFrame.
    :param df: pandas DataFrame with 'close' prices.
    :param length: The time period for the moving average.
    :param std: The number of standard deviations.
    """
    df.ta.bbands(length=length, std=std, append=True)
    return df

if __name__ == '__main__':
    # This is an example of how to use the functions.
    # It requires a running internet connection to fetch data and is for demonstration purposes.
    try:
        from src.data_acquisition.binance import fetch_ohlcv

        # Fetch some data
        data = fetch_ohlcv('BTC/USDT', '1h', 200)

        if data is not None:
            # Add indicators
            add_rsi(data)
            add_macd(data)
            add_bollinger_bands(data)

            print("DataFrame with indicators:")
            # Using .tail() to see the latest data with calculated indicators
            print(data.tail())

            # Check the new columns
            print("\nColumns added:")
            indicator_cols = [col for col in data.columns if 'RSI' in col or 'MACD' in col or 'BBL' in col or 'BBM' in col or 'BBU' in col]
            print(indicator_cols)
    except ImportError:
        print("Could not import fetch_ohlcv. Make sure you are in the correct environment.")
    except Exception as e:
        print(f"An error occurred during the example run: {e}")
