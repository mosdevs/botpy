import os
from newsapi import NewsApiClient

def fetch_news_headlines(api_key, query, page_size=100, language='en'):
    """
    Fetches news headlines for a given query using the NewsAPI.

    :param api_key: Your NewsAPI API key.
    :param query: The keyword to search for (e.g., 'Bitcoin').
    :param page_size: The number of articles to return.
    :param language: The language of the articles.
    :return: A list of article headlines, or an empty list if an error occurs.
    """
    if not api_key:
        print("Error: NewsAPI key is not provided.")
        return []

    try:
        newsapi = NewsApiClient(api_key=api_key)

        # Fetch top headlines related to the query
        top_headlines = newsapi.get_everything(
            q=query,
            language=language,
            sort_by='publishedAt', # or 'relevancy' or 'popularity'
            page_size=page_size
        )

        if top_headlines['status'] == 'ok':
            articles = top_headlines['articles']
            # We only need the titles for sentiment analysis
            headlines = [article['title'] for article in articles]
            return headlines
        else:
            print(f"Error fetching news from NewsAPI: {top_headlines.get('message')}")
            return []

    except Exception as e:
        print(f"An unexpected error occurred while fetching news: {e}")
        return []

if __name__ == '__main__':
    # Example Usage:
    # To run this, you must set the NEWS_API_KEY environment variable.
    # export NEWS_API_KEY='YOUR_KEY'

    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        print("Skipping example run: Please set the NEWS_API_KEY environment variable.")
    else:
        # Example for Bitcoin
        crypto_query = "Bitcoin"
        print(f"Fetching news for '{crypto_query}'...")
        headlines = fetch_news_headlines(api_key=api_key, query=crypto_query, page_size=5)

        if headlines:
            print("\nSuccessfully fetched headlines:")
            for i, headline in enumerate(headlines):
                print(f"{i+1}. {headline}")
        else:
            print("\nCould not fetch any headlines.")
