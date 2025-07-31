import unittest
import pandas as pd
from src.technical_analysis.indicators import add_rsi, add_macd, add_bollinger_bands

class TestTechnicalAnalysis(unittest.TestCase):

    def setUp(self):
        """
        Set up a sample DataFrame for testing.
        """
        # Create a sample DataFrame with enough data for the indicators
        data = {
            'open': [i for i in range(100)],
            'high': [i + 5 for i in range(100)],
            'low': [i - 5 for i in range(100)],
            'close': [i for i in range(100)],
            'volume': [1000 for _ in range(100)]
        }
        self.df = pd.DataFrame(data)

    def test_add_rsi(self):
        """
        Tests that the add_rsi function adds the 'RSI_14' column.
        """
        df_with_rsi = add_rsi(self.df.copy())
        self.assertIn('RSI_14', df_with_rsi.columns)
        # Check that the column has non-null values where expected
        self.assertFalse(df_with_rsi['RSI_14'].dropna().empty)

    def test_add_macd(self):
        """
        Tests that the add_macd function adds the MACD columns.
        """
        df_with_macd = add_macd(self.df.copy())
        self.assertIn('MACD_12_26_9', df_with_macd.columns)
        self.assertIn('MACDh_12_26_9', df_with_macd.columns)
        self.assertIn('MACDs_12_26_9', df_with_macd.columns)
        self.assertFalse(df_with_macd['MACD_12_26_9'].dropna().empty)

    def test_add_bollinger_bands(self):
        """
        Tests that the add_bollinger_bands function adds the Bollinger Bands columns.
        """
        df_with_bbands = add_bollinger_bands(self.df.copy())
        self.assertIn('BBL_20_2.0', df_with_bbands.columns) # Lower band
        self.assertIn('BBM_20_2.0', df_with_bbands.columns) # Middle band
        self.assertIn('BBU_20_2.0', df_with_bbands.columns) # Upper band
        self.assertFalse(df_with_bbands['BBL_20_2.0'].dropna().empty)

if __name__ == '__main__':
    unittest.main()
