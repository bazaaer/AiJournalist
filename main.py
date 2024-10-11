import os
import sys
import time
import feedparser
import markdown
from dotenv import load_dotenv
from pymongo import MongoClient

from api import (apply_tags, check_article_relevance, generate_new_article,
                 generate_new_image, generate_new_title,
                 genererate_neutral_prompt)
from upload import create_post, upload_image

# Load environment variables from .env file
load_dotenv()

# Create a MongoDB client once and reuse it
mongo_user = os.getenv("MONGO_USER", "root")
mongo_password = os.getenv("MONGO_PASSWORD", "examplepassword")
mongo_host = os.getenv("MONGO_HOST", "mongodb")
mongo_port = os.getenv("MONGO_PORT", "27017")
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
client = MongoClient(mongo_uri)
db = client.feed_monitor
articles_collection = db.articles

def save_article_entry(entry):
    articles_collection.insert_one(entry)

def entry_exists(link):
    """Check if the new entry already exists in the articles collection."""
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

def monitor_feed(feed_url, interval=10, generate_image=True, count=1):
    try:
        while True:
            # Call the updated get_latest_news to get a list of articles
            news_items = get_latest_news(feed_url, count)

            # Loop through each article in the list
            for article in news_items:
                if not entry_exists(article['link']):
                    print(f"New article found: {article['title']}")

                    # Generate AI article based on the content of the new article
                    response = check_article_relevance(article['content'])

                    if response['election_relevance']:
                        print("Article is relevant to the presidential election.")
                        ai_tags = apply_tags(article['content'])
                        print(f"Tags: {ai_tags}")
                        ai_title = generate_new_title(article['title'], article['content'])
                        ai_article = generate_new_article(article['content'])
                        ai_image_url = None
                        if generate_image:
                            neutral_prompt = genererate_neutral_prompt(article['title'])
                            try:
                                ai_image_url = generate_new_image(neutral_prompt, article['title'])
                            except Exception as e:
                                print(f"Error generating image: {e}")
                        else:
                            neutral_prompt = None

                        # Write the article to MongoDB
                        article.update({
                            'ai_title': ai_title,
                            'ai_content': ai_article,
                            'image_prompt': neutral_prompt,
                            'image': ai_image_url,
                            'tags': ai_tags,
                            'election_relevance': True
                        })
                        save_article_entry(article)

                        # Create a post on WordPress with the generated content
                        media_id = upload_image(f"image_{article['title'].lower().replace(" ", "_")}.webp", f"image_{article['title'].lower().replace(" ", "_")}.webp", "image/webp") if ai_image_url else None
                        create_post(markdown.markdown(ai_article), ai_title, media_id, ai_tags)
                    else:
                        print("Article is not relevant to the presidential election.")
                        article['election_relevance'] = False
                        save_article_entry(article)
                else:
                    print(f"Article '{article['title']}' already seen.")

            # Sleep for the defined interval before checking again
            time.sleep(interval)
            print()

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")

if __name__ == '__main__':
    url = 'https://rss.politico.com/congress.xml'
    # Get the extra parameter if provided
    article_count = sys.argv[1] if len(sys.argv) > 1 else None
    monitor_feed(url, count=int(article_count) if article_count else 1)