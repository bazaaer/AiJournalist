import os
import sys
import time
import feedparser
import markdown
from dotenv import load_dotenv
from pymongo import MongoClient
from celery import Celery

from api import (apply_tags, check_article_relevance, generate_new_article,
                 generate_new_image, generate_new_title,
                 genererate_neutral_prompt, generate_web_search)
from upload import create_post, upload_image
from websearch import search_web_image

# Load environment variables from .env file
load_dotenv()

# Configure Celery
redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = os.getenv("REDIS_PORT", "6379")
celery_app = Celery('main', broker=f'redis://{redis_host}:{redis_port}/0')
celery_app.conf.broker_connection_retry_on_startup = True

# Utility functions

def get_mongo_client():
    mongo_user = os.getenv("MONGO_USER", "root")
    mongo_password = os.getenv("MONGO_PASSWORD", "examplepassword")
    mongo_host = os.getenv("MONGO_HOST", "mongodb")
    mongo_port = os.getenv("MONGO_PORT", "27017")
    mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
    return MongoClient(mongo_uri)

def save_article_entry(entry):
    client = get_mongo_client()
    db = client.feed_monitor
    articles_collection = db.articles
    articles_collection.update_one(
        # Query to check if the article already exists
        {"link": entry["link"]},
        {"$setOnInsert": entry},  # Only insert the entry if it does not exist
        upsert=True  # Perform the upsert operation
    )

def update_article_entry(link, update_data):
    client = get_mongo_client()
    db = client.feed_monitor
    articles_collection = db.articles
    articles_collection.update_one(
        {"link": link},
        {"$set": update_data}
    )

def entry_exists(link):
    """Check if the new entry already exists in the articles collection."""
    client = get_mongo_client()
    db = client.feed_monitor
    articles_collection = db.articles
    return articles_collection.find_one({"link": link}) is not None

def get_latest_news(feed_url, count=1):
    """Get the latest news articles from a given RSS feed.

    Args:
        feed_url (str): The URL of the RSS feed.
        count (int): The number of articles to retrieve. Useful for catching up on missed articles.

    Returns:
        list: A list of dictionaries containing the article details.

    """
    feed = feedparser.parse(feed_url)
    news_items = []
    for entry in feed.entries[:count]:
        title = entry.title
        link = entry.link
        published = entry.published
        content = entry.get('content', [{'value': ''}])[0]['value']

        news_items.append({
            'title': title,
            'link': link,
            'published': published,
            'content': content
        })
    return news_items

# Celery task definitions
@celery_app.task
def process_article(article, image_option="noimg"):
    if not entry_exists(article['link']):
        print(f"New article found: {article['title']}")
        
        # Save the initial article entry
        save_article_entry(article)

        # Generate AI article based on the content of the new article
        response = check_article_relevance(article['content'])

        if response['election_relevance']:
            print("Article is relevant to the presidential election.")
            ai_tags = apply_tags(article['content'])
            print(f"Tags: {ai_tags}")
            ai_title = generate_new_title(article['title'], article['content'])
            ai_article = generate_new_article(article['content'])
            ai_image_url = None
            neutral_prompt = None
            if image_option == "aiimg":
                neutral_prompt = genererate_neutral_prompt(article['title'])
                try:
                    ai_image_url = generate_new_image(neutral_prompt, article['title'])
                except Exception as e:
                    print(f"Error generating image: {e}")
            elif image_option == "webimg":
                try:
                    web_search = generate_web_search(article['title'], article['content'])
                    search_web_image(web_search, article['title'])
                except Exception as e:
                    print(f"Error searching web image: {e}")
                neutral_prompt = None

            # Update the article entry in MongoDB
            update_data = {
                'ai_title': ai_title,
                'ai_content': ai_article,
                'image_prompt': neutral_prompt,
                'image': ai_image_url,
                'tags': ai_tags,
                'election_relevance': True
            }
            update_article_entry(article['link'], update_data)

            # Create a post on WordPress with the generated content
            if image_option in ["aiimg", "webimg"]:
                print("Uploading image...")
                try:
                    media_id = upload_image(f"image_{article['title'].lower().replace(' ', '_')}.webp", f"image_{article['title'].lower().replace(' ', '_')}.webp", "image/webp")
                except Exception as e:
                    print(f"Error uploading image: {e}")
                    media_id = None
                create_post(markdown.markdown(ai_article), ai_title, media_id, ai_tags)
            else:
                create_post(markdown.markdown(ai_article), ai_title, None, ai_tags)
        else:
            print("Article is not relevant to the presidential election.")
            update_article_entry(article['link'], {'election_relevance': False})
    else:
        print(f"Article '{article['title']}' already seen.")

# Periodic task to monitor the feed
@celery_app.task
def monitor_feed(feed_url, image_option="noimg", count=1):
    news_items = get_latest_news(feed_url, count)
    for article in news_items:
        # Queue each article individually
        process_article.delay(article, image_option)

if __name__ == '__main__':
    url = 'https://rss.politico.com/congress.xml'
    # Get the extra parameter if provided
    article_count = sys.argv[1] if len(sys.argv) > 1 else None
    image_option = sys.argv[2] if len(sys.argv) > 2 else "aiimg"
    while True:
        monitor_feed.delay(url, image_option=image_option, count=int(article_count) if article_count else 1)
        time.sleep(10)  # Run every 10 seconds