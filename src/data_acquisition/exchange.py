import ccxt
import pandas as pd

def fetch_ohlcv(exchange_name='kucoin', symbol='BTC/USDT', timeframe='1h', limit=100):
    """
    Fetches historical OHLCV data for a given symbol from a specified exchange.

    :param exchange_name: The name of the exchange (e.g., 'kucoin', 'gateio').
    :param symbol: The trading pair symbol (e.g., 'BTC/USDT').
    :param timeframe: The timeframe for the OHLCV data (e.g., '1h', '4h', '1d').
    :param limit: The number of data points to fetch.
    :return: A pandas DataFrame with OHLCV data, or None if an error occurs.
    """
    try:
        # Dynamically get the exchange class from ccxt
        exchange_class = getattr(ccxt, exchange_name)
        exchange = exchange_class()

        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        if not ohlcv:
            print(f"No OHLCV data returned from {exchange_name} for {symbol}.")
            return None

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except AttributeError:
        print(f"Error: Exchange '{exchange_name}' not found in ccxt.")
        return None
    except ccxt.NetworkError as e:
        print(f"Network Error connecting to {exchange_name}: {e}")
        return None
    except ccxt.ExchangeError as e:
        print(f"Exchange Error with {exchange_name}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage with the default exchange (KuCoin)
    print("--- Fetching data from KuCoin (default) ---")
    btc_ohlcv_kucoin = fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=5)
    if btc_ohlcv_kucoin is not None:
        print("Successfully fetched BTC/USDT 1-hour OHLCV data from KuCoin:")
        print(btc_ohlcv_kucoin.head())

    print("\n--- Fetching data from Gate.io (alternative) ---")
    # Example usage with a different exchange
    btc_ohlcv_gateio = fetch_ohlcv(exchange_name='gateio', symbol='BTC_USDT', timeframe='1h', limit=5)
    if btc_ohlcv_gateio is not None:
        print("Successfully fetched BTC_USDT 1-hour OHLCV data from Gate.io:")
        print(btc_ohlcv_gateio.head())
