import unittest
import pandas as pd
from src.trading_strategy.simple_strategy import generate_signal

class TestTradingStrategy(unittest.TestCase):

    def setUp(self):
        """Set up a base DataFrame for buy and sell scenarios."""
        self.buy_technicals_df = pd.DataFrame({
            'RSI_14': [40, 25],          # Crosses below 30
            'MACD_12_26_9': [-0.5, 0.5], # Crosses up
            'MACDs_12_26_9': [0, 0]
        })
        self.sell_technicals_df = pd.DataFrame({
            'RSI_14': [60, 75],          # Crosses above 70
            'MACD_12_26_9': [0.5, -0.5], # Crosses down
            'MACDs_12_26_9': [0, 0]
        })

    def test_generate_signal_buy(self):
        """Tests that a 'buy' signal is generated when all conditions are met."""
        # Positive sentiment should trigger a buy
        self.assertEqual(generate_signal(self.buy_technicals_df, sentiment_score=0.5), 'buy')

    def test_generate_signal_sell(self):
        """Tests that a 'sell' signal is generated when all conditions are met."""
        # Negative sentiment should trigger a sell
        self.assertEqual(generate_signal(self.sell_technicals_df, sentiment_score=-0.5), 'sell')

    def test_generate_signal_hold_due_to_sentiment(self):
        """Tests for 'hold' when technicals are met but sentiment is not."""
        # Technicals are good for a buy, but sentiment is too low (neutral)
        self.assertEqual(generate_signal(self.buy_technicals_df, sentiment_score=0.1), 'hold')
        # Technicals are good for a buy, but sentiment is negative
        self.assertEqual(generate_signal(self.buy_technicals_df, sentiment_score=-0.5), 'hold')

        # Technicals are good for a sell, but sentiment is too low (neutral)
        self.assertEqual(generate_signal(self.sell_technicals_df, sentiment_score=-0.1), 'hold')
        # Technicals are good for a sell, but sentiment is positive
        self.assertEqual(generate_signal(self.sell_technicals_df, sentiment_score=0.5), 'hold')

    def test_generate_signal_hold_due_to_technicals(self):
        """Tests for 'hold' when sentiment is good but technicals are not."""
        # No MACD crossover
        no_crossover_df = pd.DataFrame({
            'RSI_14': [40, 25], 'MACD_12_26_9': [0.1, 0.5], 'MACDs_12_26_9': [0, 0]
        })
        self.assertEqual(generate_signal(no_crossover_df, sentiment_score=0.8), 'hold')

        # RSI condition not met
        rsi_fail_df = pd.DataFrame({
            'RSI_14': [40, 45], 'MACD_12_26_9': [-0.5, 0.5], 'MACDs_12_26_9': [0, 0]
        })
        self.assertEqual(generate_signal(rsi_fail_df, sentiment_score=0.8), 'hold')

    def test_generate_signal_hold_insufficient_data(self):
        """Tests for 'hold' when there is not enough data."""
        one_row_df = self.buy_technicals_df.head(1)
        self.assertEqual(generate_signal(one_row_df, sentiment_score=0.8), 'hold')

        empty_df = pd.DataFrame()
        self.assertEqual(generate_signal(empty_df, sentiment_score=0.8), 'hold')

    def test_generate_signal_hold_missing_columns(self):
        """Tests for 'hold' when required columns are missing."""
        missing_cols_df = pd.DataFrame({'RSI_14': [40, 25]})
        self.assertEqual(generate_signal(missing_cols_df, sentiment_score=0.8), 'hold')

    def test_generate_signal_with_nan_values(self):
        """Tests for 'hold' when there are NaN values in the latest row."""
        nan_df = pd.DataFrame({
            'RSI_14': [40, None], 'MACD_12_26_9': [-0.5, 0.5], 'MACDs_12_26_9': [0, 0]
        })
        self.assertEqual(generate_signal(nan_df, sentiment_score=0.8), 'hold')

if __name__ == '__main__':
    unittest.main()
