import pandas as pd

# --- Strategy Parameters ---
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
SENTIMENT_BUY_THRESHOLD = 0.2
SENTIMENT_SELL_THRESHOLD = -0.2

def generate_signal(df, sentiment_score):
    """
    Generates a trading signal based on technical indicators and sentiment score.

    The strategy is as follows:
    - Buy Signal: RSI is below 30 AND MACD crosses above signal AND sentiment is positive.
    - Sell Signal: RSI is above 70 AND MACD crosses below signal AND sentiment is negative.
    - Hold Signal: Otherwise.

    :param df: A pandas DataFrame containing OHLCV data and technical indicators.
    :param sentiment_score: A float representing the current sentiment score (-1 to 1).
    :return: A string: 'buy', 'sell', or 'hold'.
    """
    # Make sure there are at least two rows to check for a crossover and all columns are present
    required_cols = ['RSI_14', 'MACD_12_26_9', 'MACDs_12_26_9']
    if len(df) < 2 or not all(col in df.columns for col in required_cols):
        return 'hold'

    # Get the last two rows of data
    latest_data = df.iloc[-1]
    previous_data = df.iloc[-2]

    # Check for NaN values in the latest data point for required columns
    if latest_data[required_cols].isnull().any():
        return 'hold'

    # --- Technical Indicator Conditions ---
    rsi_buy_condition = latest_data['RSI_14'] < RSI_OVERSOLD
    rsi_sell_condition = latest_data['RSI_14'] > RSI_OVERBOUGHT

    macd_line_col = 'MACD_12_26_9'
    signal_line_col = 'MACDs_12_26_9'
    macd_cross_above = (previous_data[macd_line_col] < previous_data[signal_line_col]) and \
                       (latest_data[macd_line_col] > latest_data[signal_line_col])
    macd_cross_below = (previous_data[macd_line_col] > previous_data[signal_line_col]) and \
                       (latest_data[macd_line_col] < latest_data[signal_line_col])

    # --- Sentiment Conditions ---
    sentiment_buy_condition = sentiment_score > SENTIMENT_BUY_THRESHOLD
    sentiment_sell_condition = sentiment_score < SENTIMENT_SELL_THRESHOLD

    # --- Combine conditions for final signal ---
    if rsi_buy_condition and macd_cross_above and sentiment_buy_condition:
        return 'buy'
    elif rsi_sell_condition and macd_cross_below and sentiment_sell_condition:
        return 'sell'
    else:
        return 'hold'

if __name__ == '__main__':
    # Example Usage

    # --- Create a sample DataFrame ---
    sample_data = {
        'RSI_14': [40, 25], # RSI crosses into oversold
        'MACD_12_26_9': [-0.5, 0.5], # MACD crosses up
        'MACDs_12_26_9': [0, 0]
    }
    sample_df = pd.DataFrame(sample_data)

    print("--- Testing Scenarios ---")

    # Scenario 1: All conditions met for a BUY
    positive_sentiment = 0.5
    signal = generate_signal(sample_df, positive_sentiment)
    print(f"With positive sentiment ({positive_sentiment}), signal is: {signal.upper()}") # Expected: BUY

    # Scenario 2: Sentiment is not strong enough for a BUY
    neutral_sentiment = 0.1
    signal = generate_signal(sample_df, neutral_sentiment)
    print(f"With neutral sentiment ({neutral_sentiment}), signal is: {signal.upper()}") # Expected: HOLD

    # Scenario 3: All conditions met for a SELL
    sell_data = {
        'RSI_14': [60, 75], # RSI crosses into overbought
        'MACD_12_26_9': [0.5, -0.5], # MACD crosses down
        'MACDs_12_26_9': [0, 0]
    }
    sell_df = pd.DataFrame(sell_data)
    negative_sentiment = -0.6
    signal = generate_signal(sell_df, negative_sentiment)
    print(f"With negative sentiment ({negative_sentiment}), signal is: {signal.upper()}") # Expected: SELL

    # Scenario 4: Technicals suggest BUY, but sentiment is negative
    signal = generate_signal(sample_df, negative_sentiment)
    print(f"With conflicting negative sentiment ({negative_sentiment}), signal is: {signal.upper()}") # Expected: HOLD
