import unittest
from unittest.mock import patch, MagicMock

# Test News Fetcher
from src.sentiment_analysis.news_fetcher import fetch_news_headlines

# Test Analyzer
from src.sentiment_analysis.analyzer import SentimentAnalyzer
import torch

class TestSentimentAnalysis(unittest.TestCase):

    @patch('src.sentiment_analysis.news_fetcher.NewsApiClient')
    def test_fetch_news_headlines_success(self, MockNewsApiClient):
        """
        Tests that news headlines are fetched and processed correctly on success.
        """
        # Configure the mock
        mock_instance = MockNewsApiClient.return_value
        mock_instance.get_everything.return_value = {
            'status': 'ok',
            'articles': [
                {'title': 'Headline 1'},
                {'title': 'Headline 2'}
            ]
        }

        headlines = fetch_news_headlines('fake_api_key', 'test_query')

        self.assertEqual(len(headlines), 2)
        self.assertEqual(headlines[0], 'Headline 1')
        MockNewsApiClient.assert_called_once_with(api_key='fake_api_key')
        mock_instance.get_everything.assert_called_once()

    @patch('src.sentiment_analysis.news_fetcher.NewsApiClient')
    def test_fetch_news_headlines_error(self, MockNewsApiClient):
        """
        Tests that an empty list is returned on API error.
        """
        mock_instance = MockNewsApiClient.return_value
        mock_instance.get_everything.return_value = {'status': 'error', 'message': 'Test error'}

        headlines = fetch_news_headlines('fake_api_key', 'test_query')
        self.assertEqual(headlines, [])

    @patch('src.sentiment_analysis.analyzer.AutoModelForSequenceClassification.from_pretrained')
    @patch('src.sentiment_analysis.analyzer.AutoTokenizer.from_pretrained')
    def test_sentiment_analyzer(self, MockTokenizer, MockModel):
        """
        Tests the SentimentAnalyzer class with mocked model and tokenizer.
        """
        # Configure mocks
        MockTokenizer.return_value = MagicMock()
        mock_model_instance = MockModel.return_value

        # Mock the model's output (logits)
        # Let's create a sample output for a batch of 2 headlines
        mock_logits = torch.tensor([
            [0.9, 0.1, 0.0],  # Headline 1: Very positive
            [0.1, 0.9, 0.0]   # Headline 2: Very negative
        ])
        # The model output is an object with a 'logits' attribute
        mock_output = MagicMock()
        mock_output.logits = mock_logits
        mock_model_instance.return_value = mock_output

        # Initialize the analyzer (this will use the mocks)
        analyzer = SentimentAnalyzer()
        self.assertIsNotNone(analyzer.model, "Model should be mocked, not None")

        headlines = ["A very positive story", "A very negative story"]
        score = analyzer.analyze_sentiment(headlines)

        # Let's calculate the expected score.
        # The softmax will turn logits into probabilities.
        # Then we compute `pos_prob - neg_prob` for each and average them.
        # For [0.9, 0.1], pos_prob is high, neg_prob is low. Score is positive.
        # For [0.1, 0.9], pos_prob is low, neg_prob is high. Score is negative.
        # The average of a positive and a negative number of same magnitude should be near 0.
        self.assertIsInstance(score, float)
        self.assertAlmostEqual(score, 0.0, places=2)

        # Test with a clearly positive set of headlines
        mock_logits_positive = torch.tensor([
            [0.9, 0.1, 0.0],
            [0.8, 0.2, 0.0]
        ])
        mock_output.logits = mock_logits_positive
        score_positive = analyzer.analyze_sentiment(headlines)
        self.assertGreater(score_positive, 0)


if __name__ == '__main__':
    unittest.main()
