# Crypto Trading Bot with Sentiment Analysis

This project is a Python-based cryptocurrency trading bot that uses a combination of technical analysis and news sentiment analysis to generate trading signals. It fetches market data from KuCoin (by default), calculates technical indicators, analyzes the sentiment of recent news headlines, and sends trading alerts via a Telegram bot.

## Features

- **Flexible Data Source:** Fetches market data from KuCoin by default, but can be easily configured to use any other exchange supported by the `ccxt` library.
- **Technical Analysis:** Calculates RSI, MACD, and Bollinger Bands from market data.
- **Sentiment Analysis:** Fetches crypto-related news from NewsAPI and analyzes the sentiment of the headlines using the `ProsusAI/finbert` model from Hugging Face.
- **Combined Strategy:** Generates `BUY` or `SELL` signals only when both technical indicators and news sentiment are aligned.
- **Telegram Alerts:** Sends formatted trading signals directly to your Telegram chat or channel.
- **Modular Design:** The code is organized into separate, reusable modules for data acquisition, technical analysis, sentiment analysis, and notifications.
- **Unit Tested:** Comes with a suite of unit tests to ensure the reliability of each component.

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/botpy.git
cd botpy
```

### 2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all the required Python libraries from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```
*Note: The first time you run the bot, the sentiment analysis model (`~400MB`) will be downloaded. This may take a few minutes.*

## Configuration

This bot requires three environment variables to be set. You can set them in your shell or use a `.env` file with a library like `python-dotenv`.

- **`TELEGRAM_BOT_TOKEN`**: Your Telegram bot's API token. You can get this from the BotFather on Telegram.
- **`TELEGRAM_CHAT_ID`**: The ID of the Telegram chat, channel, or user you want to send messages to.
- **`NEWS_API_KEY`**: Your API key from [newsapi.org](https://newsapi.org). A free developer plan is available.

**Example of setting environment variables:**
```bash
export TELEGRAM_BOT_TOKEN='your_telegram_token'
export TELEGRAM_CHAT_ID='your_chat_id'
export NEWS_API_KEY='your_news_api_key'
```

## Usage

To run the trading bot, execute the `main.py` script from the root directory:
```bash
python3 src/main.py
```
The bot will start and print its progress to the console, checking for signals at the interval defined in `src/main.py`.

### Changing the Exchange
The bot uses KuCoin by default. To use a different exchange, simply change the `EXCHANGE_NAME` variable at the top of the `src/main.py` file to any other exchange supported by `ccxt` (e.g., `'gateio'`, `'bybit'`).

## Running Tests

To run the full suite of unit tests, use the `unittest` module's discovery feature:
```bash
python3 -m unittest discover tests
```
This will run all test files located in the `tests/` directory.

## Disclaimer

This trading bot is for educational and experimental purposes only. Automated trading involves significant financial risk. The creators of this bot are not responsible for any financial losses you may incur. Always do your own research and never trade with money you cannot afford to lose.
