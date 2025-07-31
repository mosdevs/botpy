import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from src.telegram_bot.bot import send_message

class TestTelegramBot(unittest.TestCase):

    @patch('src.telegram_bot.bot.telegram.Bot')
    def test_send_message_success(self, MockBot):
        """
        Tests successful message sending.
        """
        # Configure the mock
        mock_bot_instance = MockBot.return_value
        mock_bot_instance.send_message = AsyncMock()

        # Run the async function
        result = asyncio.run(send_message('fake_token', '12345', 'test message'))

        # Assertions
        self.assertTrue(result)
        MockBot.assert_called_once_with(token='fake_token')
        mock_bot_instance.send_message.assert_awaited_once_with(chat_id='12345', text='test message')

    def test_send_message_missing_credentials(self):
        """
        Tests that sending fails if token or chat_id is missing.
        """
        # Test with missing token
        result = asyncio.run(send_message(None, '12345', 'test'))
        self.assertFalse(result)

        # Test with missing chat_id
        result = asyncio.run(send_message('fake_token', None, 'test'))
        self.assertFalse(result)

    @patch('src.telegram_bot.bot.telegram.Bot')
    def test_send_message_telegram_error(self, MockBot):
        """
        Tests the handling of a Telegram API error.
        """
        # Import the error class here to avoid potential circular imports if it was at the top
        from telegram.error import TelegramError

        # Configure the mock to raise an error
        mock_bot_instance = MockBot.return_value
        mock_bot_instance.send_message = AsyncMock(side_effect=TelegramError("Test error"))

        # Run the async function
        result = asyncio.run(send_message('fake_token', '12345', 'test message'))

        # Assertions
        self.assertFalse(result)
        MockBot.assert_called_once_with(token='fake_token')
        mock_bot_instance.send_message.assert_awaited_once()

if __name__ == '__main__':
    unittest.main()
