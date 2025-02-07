import numpy as np
import pandas as pd
from typing import Optional, List
import os
import logging
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import requests  # <-- Add this line
from io import BytesIO
import random


# Load environment variables from the .env file
load_dotenv()

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get News API credentials from environment variables with error handling
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Ensure NLTK data is available
nltk.download('vader_lexicon')
# Cache for latest news
news_cache = {
    "timestamp": None,
    "articles": None
}

def generate_topic():
    """
    Generate a random topic for a tweet from a predefined list of topics.
    """
            
    
    topics = [
       "Entrepreneurshit", "Startup Culture", "indie development studio Bootstrapping techniques"
"Art","Digital art trend", "traditional art trend", "Comic book illutration trends", "Inking tips and tricks"
"Technology updates", "AI trends","NVIDIA updates and News", "Unreal Engine Updates and News","Indie Game development News", 
"AI and traditional art", "generative Ai news and updates","comic book culture", "Grafitti culture", 
"Heavy Metal Magazine Culture", "SciFi", "Cinematis and VFXs","Street Art"
    ]

    topic = random.choice(topics)
    logger.info(f"Selected random topic: {topic}")
    return topic

def fetch_latest_news(top_n: int = 15) -> Optional[list]:
    """
    Fetch the latest news articles about Bitcoin in English.
    Returns a list of up to 'top_n' articles.
    """
    news_topic = generate_topic()
    current_time = datetime.now()
    if news_cache["timestamp"] and (current_time - news_cache["timestamp"]) < timedelta(minutes=25):
        logger.info("Using cached news articles.")
        return news_cache["articles"][:top_n]  # Return only the top_n cached articles

    logger.info(f"Fetching latest {news_topic} news...")
    url = f"https://newsapi.org/v2/everything?q={news_topic}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        news_cache["timestamp"] = current_time
        news_cache["articles"] = articles
        logger.info(f"Successfully fetched {len(articles)} news articles.")

        # Log the titles and URLs of the articles
        for article in articles[:top_n]:  # Log only the top_n articles
            title = article.get('title', 'No Title Available')
            article_url = article.get('url', 'No URL Available')
            logger.info(f"Article Title: {title}")
            logger.info(f"Article URL: {article_url}")

        return articles[:top_n]  # Return only the top_n articles
    else:
        logger.error(f"Failed to fetch news. Status code: {response.status_code}")
        return None


def extract_image(article) -> Optional[str]:
    """
    Extract the URL of the image from the news article.
    """
    image_url = article.get('urlToImage', None)
    if image_url:
        logger.info(f"Extracted image URL: {image_url}")
    else:
        logger.warning("No image found in the article.")
    return image_url
