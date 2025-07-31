import os
import telegram
import asyncio

async def send_message(token, chat_id, text):
    """
    Sends a message to a specified Telegram chat.

    :param token: The Telegram Bot API token.
    :param chat_id: The ID of the chat to send the message to.
    :param text: The message text to send.
    :return: True if the message was sent successfully, False otherwise.
    """
    if not token or not chat_id:
        print("Error: Telegram token or chat ID is not configured.")
        return False

    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=text)
        print(f"Successfully sent message to chat_id {chat_id}")
        return True
    except telegram.error.TelegramError as e:
        print(f"Error sending Telegram message: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

async def main():
    """
    Example usage of the send_message function.
    Reads token and chat_id from environment variables.
    """
    # In a real application, use a secure way to manage your token
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    # This can be a channel ID (e.g., '@mychannel') or a user ID
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        print("Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables to run this example.")
        return

    test_message = "Hello from the trading bot! This is a test message."
    await send_message(token, chat_id, test_message)

if __name__ == '__main__':
    # To run this example, you need to set the environment variables:
    # export TELEGRAM_BOT_TOKEN='YOUR_TOKEN'
    # export TELEGRAM_CHAT_ID='YOUR_CHAT_ID'
    # The asyncio.run() is used to execute the async main function.
    # Note: This will fail if the environment variables are not set.
    if os.environ.get('TELEGRAM_BOT_TOKEN') and os.environ.get('TELEGRAM_CHAT_ID'):
        asyncio.run(main())
    else:
        print("Skipping example run: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID not set.")
