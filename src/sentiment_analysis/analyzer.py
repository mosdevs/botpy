from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAnalyzer:
    """
    A class to analyze the sentiment of financial news headlines using a pre-trained model.
    """
    def __init__(self, model_name='ProsusAI/finbert'):
        """
        Initializes the tokenizer and model.
        This can take some time as it might need to download the model.
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            print(f"Successfully loaded model and tokenizer for '{model_name}'.")
        except Exception as e:
            print(f"Error loading Hugging Face model: {e}")
            # Set to None if loading fails, so we can handle it gracefully
            self.tokenizer = None
            self.model = None

    def analyze_sentiment(self, headlines):
        """
        Analyzes the sentiment of a list of headlines.

        :param headlines: A list of strings (news headlines).
        :return: An average sentiment score between -1 (negative) and 1 (positive),
                 or 0 if no headlines are provided or the model isn't loaded.
        """
        if not self.model or not self.tokenizer or not headlines:
            return 0.0

        try:
            # Tokenize the headlines. It's better to process them in a batch.
            inputs = self.tokenizer(headlines, padding=True, truncation=True, return_tensors='pt', max_length=512)

            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Convert logits to probabilities
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # The model's label mapping is: 0 -> positive, 1 -> negative, 2 -> neutral
            # We calculate a score for each headline: positive_prob - negative_prob
            # This gives a score from -1 to 1 for each headline
            sentiment_scores = predictions[:, 0] - predictions[:, 1]

            # Calculate the average score across all headlines
            average_score = sentiment_scores.mean().item()

            return average_score

        except Exception as e:
            print(f"An error occurred during sentiment analysis: {e}")
            return 0.0

if __name__ == '__main__':
    # This block will run on first import and may download the model.
    # This can take a while and a significant amount of disk space.
    print("Initializing Sentiment Analyzer (this may download the model)...")
    analyzer = SentimentAnalyzer()

    if analyzer.model:
        # Example headlines
        sample_headlines = [
            "Bitcoin surges past $50,000, investors are bullish",
            "Ethereum price drops sharply after network congestion issues",
            "Crypto market remains stable with low volatility"
        ]

        print("\nAnalyzing sample headlines:")
        # Analyze all at once to get the average
        average_score = analyzer.analyze_sentiment(sample_headlines)
        print(f"Average sentiment score for all headlines: {average_score:.3f}")

        # Example of a single headline
        single_headline = ["Analysts predict a strong rally for altcoins next quarter."]
        single_score = analyzer.analyze_sentiment(single_headline)
        print(f"\nSentiment for '{single_headline[0]}': {single_score:.3f}")
    else:
        print("\nCould not run example because the sentiment model failed to load.")
