import os
import asyncio
import pandas as pd
from dotenv import load_dotenv

load_dotenv(dotenv_path='D:/Jules/BotPy/botpy/.env')  # use absolute path to be sure

print(os.getenv('TELEGRAM_BOT_TOKEN'))

# Import functions from our modules
from src.data_acquisition.binance import fetch_ohlcv
from src.technical_analysis.indicators import add_rsi, add_macd, add_bollinger_bands
from src.trading_strategy.simple_strategy import generate_signal
from src.telegram_bot.bot import send_message
from src.sentiment_analysis.news_fetcher import fetch_news_headlines
from src.sentiment_analysis.analyzer import SentimentAnalyzer

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

print("Token:", TELEGRAM_BOT_TOKEN)  # optional: test if it works

# --- Configuration ---
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'
NEWS_QUERY = 'Bitcoin'  # Query for fetching news articles for sentiment analysis
DATA_LIMIT = 200
CHECK_INTERVAL_SECONDS = 300  # 5 minutes

async def check_for_signals(analyzer, news_api_key):
    """
    The main logic loop for the trading bot.
    Fetches data, analyzes it, and sends a signal if necessary.
    """
    print(f"--- Checking for signals for {SYMBOL} at {pd.Timestamp.now()} ---")

    # 1. Fetch Market Data
    market_data = fetch_ohlcv(symbol=SYMBOL, timeframe=TIMEFRAME, limit=DATA_LIMIT)
    if market_data is None or market_data.empty:
        print("Could not fetch market data. Skipping this check.")
        return

    # 2. Fetch and Analyze News Sentiment
    print(f"Fetching news for '{NEWS_QUERY}'...")
    headlines = fetch_news_headlines(api_key=news_api_key, query=NEWS_QUERY)
    if not headlines:
        print("Could not fetch news headlines. Proceeding without sentiment.")
        sentiment_score = 0.0 # Neutral sentiment if no news
    else:
        sentiment_score = analyzer.analyze_sentiment(headlines)
        print(f"Calculated sentiment score: {sentiment_score:.3f}")

    # 3. Calculate Technical Indicators
    add_rsi(market_data)
    add_macd(market_data)
    add_bollinger_bands(market_data)

    # 4. Generate Signal using both technicals and sentiment
    signal = generate_signal(market_data, sentiment_score)
    print(f"Generated signal: {signal.upper()}")

    # 5. Send Telegram Alert
    if signal in ['buy', 'sell']:
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')

        if not token or not chat_id:
            print("Telegram credentials not found. Cannot send alert.")
            return

        latest_price = market_data['close'].iloc[-1]
        message = f"""
🚨 Trading Signal Alert 🚨

Symbol: {SYMBOL}
Signal: {signal.upper()}
Price: ${latest_price:,.2f}
Sentiment Score: {sentiment_score:.3f}
Timeframe: {TIMEFRAME}
"""
        await send_message(token, chat_id, message)
    else:
        print("Signal is 'hold'. No action required.")


async def main():
    """
    The main entry point for the bot. Initializes modules and runs the loop.
    """
    print("Initializing sentiment analyzer (this may take a moment)...")
    analyzer = SentimentAnalyzer()
    if not analyzer.model:
        print("Failed to load sentiment model. The bot cannot run.")
        return

    news_api_key = os.environ.get("NEWS_API_KEY")
    if not news_api_key:
        print("NEWS_API_KEY not found in environment variables. The bot cannot run.")
        return

    print("Starting trading bot...")
    while True:
        try:
            await check_for_signals(analyzer, news_api_key)
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")

        print(f"Waiting for {CHECK_INTERVAL_SECONDS} seconds...")
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == '__main__':
    print("Trading Bot Main Script")
    print("-----------------------")
    print("This script integrates all modules to run the trading bot.")
    print("\nRequired Environment Variables:")
    print(" - TELEGRAM_BOT_TOKEN: Your Telegram bot's API token.")
    print(" - TELEGRAM_CHAT_ID: The chat ID to send messages to.")
    print(" - NEWS_API_KEY: Your API key from newsapi.org.")

    # Due to network/API restrictions in this sandbox, we cannot run the live bot.
    # The following lines show how a user would start the bot.
    #
    # if "NEWS_API_KEY" not in os.environ:
    #     print("\nError: NEWS_API_KEY is not set. Please set it to run the bot.")
    # else:
    #     try:
    #         asyncio.run(main())
    #     except KeyboardInterrupt:
    #         print("\nBot stopped by user.")

    print("\nTo start the bot, ensure all environment variables are set and uncomment the asyncio.run(main()) lines in a live environment.")
