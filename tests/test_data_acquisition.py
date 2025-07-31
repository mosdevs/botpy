import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.data_acquisition.binance import fetch_ohlcv

class TestDataAcquisition(unittest.TestCase):

    @patch('src.data_acquisition.binance.ccxt.binance')
    def test_fetch_ohlcv(self, mock_binance):
        """
        Tests the fetch_ohlcv function from the binance module with a mock.
        """
        # Create a mock instance of the binance exchange
        mock_exchange = MagicMock()

        # Sample OHLCV data to be returned by the mock
        sample_ohlcv = [
            [1622505600000, 30000, 31000, 29000, 30500, 1000],
            [1622509200000, 30500, 31500, 30000, 31000, 1200],
        ]

        # Configure the mock to return the sample data
        mock_exchange.fetch_ohlcv.return_value = sample_ohlcv
        mock_binance.return_value = mock_exchange

        # Test with default parameters
        df = fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=2)

        # Assertions
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['open', 'high', 'low', 'close', 'volume'])

        # Verify that the mock was called correctly
        mock_binance.assert_called_once()
        mock_exchange.fetch_ohlcv.assert_called_once_with('BTC/USDT', '1h', limit=2)

        # Test with different parameters
        mock_exchange.fetch_ohlcv.reset_mock()
        sample_eth_ohlcv = [[1622505600000, 2000, 2100, 1900, 2050, 5000]]
        mock_exchange.fetch_ohlcv.return_value = sample_eth_ohlcv

        df_eth = fetch_ohlcv(symbol='ETH/USDT', timeframe='4h', limit=1)
        self.assertIsNotNone(df_eth)
        self.assertIsInstance(df_eth, pd.DataFrame)
        self.assertEqual(len(df_eth), 1)
        mock_exchange.fetch_ohlcv.assert_called_once_with('ETH/USDT', '4h', limit=1)


if __name__ == '__main__':
    unittest.main()
