import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.data_acquisition.exchange import fetch_ohlcv

class TestExchange(unittest.TestCase):

    @patch('src.data_acquisition.exchange.getattr')
    def test_fetch_ohlcv_default_kucoin(self, mock_getattr):
        """
        Tests the fetch_ohlcv function using the default KuCoin exchange.
        """
        # --- Setup Mock ---
        mock_kucoin_class = MagicMock()
        mock_kucoin_instance = MagicMock()

        # Sample OHLCV data to be returned by the mock
        sample_ohlcv = [
            [1622505600000, 30000, 31000, 29000, 30500, 1000],
            [1622509200000, 30500, 31500, 30000, 31000, 1200],
        ]
        mock_kucoin_instance.fetch_ohlcv.return_value = sample_ohlcv

        # Configure the mock chain: getattr -> ExchangeClass() -> instance
        mock_kucoin_class.return_value = mock_kucoin_instance
        mock_getattr.return_value = mock_kucoin_class

        # --- Call Function ---
        # Call with default parameters (should use 'kucoin')
        df = fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=2)

        # --- Assertions ---
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['open', 'high', 'low', 'close', 'volume'])

        # Verify that getattr was called with 'kucoin'
        mock_getattr.assert_called_once_with(unittest.mock.ANY, 'kucoin')
        mock_kucoin_instance.fetch_ohlcv.assert_called_once_with('BTC/USDT', '1h', limit=2)

    @patch('src.data_acquisition.exchange.getattr')
    def test_fetch_ohlcv_dynamic_exchange(self, mock_getattr):
        """
        Tests that the function can dynamically call a different exchange.
        """
        # --- Setup Mock for Gate.io ---
        mock_gateio_class = MagicMock()
        mock_gateio_instance = MagicMock()
        mock_gateio_instance.fetch_ohlcv.return_value = [[1622505600000, 1, 2, 0, 1, 100]]
        mock_gateio_class.return_value = mock_gateio_instance
        mock_getattr.return_value = mock_gateio_class

        # --- Call Function ---
        df = fetch_ohlcv(exchange_name='gateio', symbol='BTC_USDT', timeframe='1h', limit=1)

        # --- Assertions ---
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 1)
        mock_getattr.assert_called_once_with(unittest.mock.ANY, 'gateio')
        mock_gateio_instance.fetch_ohlcv.assert_called_once_with('BTC_USDT', '1h', limit=1)

    def test_fetch_ohlcv_invalid_exchange(self):
        """
        Tests that the function returns None for a non-existent exchange.
        """
        # ccxt will raise an AttributeError for an invalid exchange name
        df = fetch_ohlcv(exchange_name='invalid_exchange_name')
        self.assertIsNone(df)

if __name__ == '__main__':
    unittest.main()
