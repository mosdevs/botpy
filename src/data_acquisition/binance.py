import ccxt
import pandas as pd

def fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=100):
    """
    Fetches historical OHLCV data for a given symbol from Binance.

    :param symbol: The trading pair symbol (e.g., 'BTC/USDT').
    :param timeframe: The timeframe for the OHLCV data (e.g., '1h', '4h', '1d').
    :param limit: The number of data points to fetch.
    :return: A pandas DataFrame with OHLCV data, or None if an error occurs.
    """
    try:
        binance = ccxt.binance()
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except ccxt.NetworkError as e:
        print(f"Network Error: {e}")
        return None
    except ccxt.ExchangeError as e:
        print(f"Exchange Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    btc_ohlcv = fetch_ohlcv('BTC/USDT', '1h', 100)
    if btc_ohlcv is not None:
        print("Successfully fetched BTC/USDT 1-hour OHLCV data:")
        print(btc_ohlcv.head())
        print("...")
        print(btc_ohlcv.tail())
