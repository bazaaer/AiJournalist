import time
import re
import json
import os
from datetime import datetime
import requests
import feedparser
import sys
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from api import generate_new_image, genererate_neutral_prompt, check_article_relevance, generate_new_article, generate_new_title

from upload import create_post, upload_image


def save_seen_entries(seen_entries, last_id, file_path="seen_entries.json"):
    data = {
        'seen_entries': seen_entries,
        'last_id': last_id
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def load_seen_entries(file_path="seen_entries.json"):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            seen_entries = data.get('seen_entries', [])
            last_id = data.get('last_id', 0)
    else:
        seen_entries = []
        last_id = 0

    return seen_entries, last_id


def entry_exists(seen_entries, new_entry):
    """Check if the new entry already exists in the seen entries."""
    for entry in seen_entries:
        if entry['link'] == new_entry['link']:  # Use link or another identifier to check
            return True
    return False


def remove_html_tags(text):
    """Remove HTML tags from a string."""
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text


def write_article_to_file(article_id, ai_title, ai_article, image_prompt, ai_image_url, file_path):
    # Create a dictionary with the article details
    article_data = {
        'id': article_id,
        'title': ai_title,
        'content': ai_article,
        'image_prompt': image_prompt,
        'image': ai_image_url
    }

    # Check if the file already exists
    if os.path.exists(file_path):
        # If the file exists, load its current contents
        with open(file_path, 'r') as file:
            try:
                articles = json.load(file)
            except json.JSONDecodeError:
                # If the file is empty or corrupted, start fresh
                articles = []
    else:
        # If the file does not exist, start with an empty list
        articles = []

    # Add the new article to the list of articles
    articles.append(article_data)

    # Write the updated articles list back to the file
    with open(file_path, 'w') as file:
        json.dump(articles, file, indent=4)

    print(f"Article {article_id} saved to {file_path}.")


def get_latest_news(feed_url, count=1):
    """Get the latest news articles from a given RSS feed.
    
    Args:
        feed_url (str): The URL of the RSS feed.
        count (int): The number of articles to retrieve. Usefull for catching up on missed articles.
        
    Returns:
        list: A list of dictionaries containing the article details.
        
    """

    feed = feedparser.parse(feed_url)
    news_items = []

    for entry in feed.entries[:count]:
        title = entry.title
        link = entry.link
        published = entry.published
        content = None
        if hasattr(entry, 'content'):
            content = entry.content[0].value
            content = remove_html_tags(content)

        news_items.append({
            'title': title,
            'link': link,
            'published': published,
            'content': content
        })

    return news_items


def monitor_feed(feed_url, interval=10, genertate_image=True, count=1):
    seen_entries, last_id = load_seen_entries()

    try:
        while True:
            # Call the updated get_latest_news to get a list of articles
            news_items = get_latest_news(feed_url, count)

            # Loop through each article in the list
            for article in news_items:
                new_entry = {'id': last_id + 1,
                             'title': article['title'],
                             'link': article['link'],
                             'published': article['published'],
                             'content': article['content']}

                if not entry_exists(seen_entries, new_entry):
                    last_id = last_id + 1
                    seen_entries.append(new_entry)
                    print(f"New article found: {article['title']}")

                    # Generate AI article based on the content of the new article
                    response = check_article_relevance(new_entry['content'])

                    if response['election_relevance']:
                        print("Article is relevant to the presidential election.")
                        ai_title = generate_new_title(new_entry['title'], new_entry['content'])
                        ai_article = generate_new_article(new_entry['content'])
                        neutral_prompt = genererate_neutral_prompt(new_entry['title'])
                        if genertate_image:
                            try:
                                ai_image_url = generate_new_image(neutral_prompt, last_id)
                            except Exception as e:
                                print(f"Error generating image: {e}")
                                ai_image_url = None
                        else:
                            ai_image_url = None

                        # Write the article to the file
                        write_article_to_file(
                            last_id, ai_title, ai_article, neutral_prompt, ai_image_url, "generated_articles.json")
                        
                        # Create a post on WordPress with the generated content
                        if ai_image_url:
                            media_id = upload_image(f"image_{last_id}.jpg", f"image_{last_id}.jpg", "image/jpeg")
                            create_post(ai_article, ai_title, media_id)
                        else:
                            media_id = None
                            create_post(ai_article, ai_title, media_id)
                        
                    else:
                        print("Article is not relevant to the presidential election.")
                        pass

                else:
                    print(f"Article '{article['title']}' already seen.")

            # Sleep for the defined interval before checking again
            time.sleep(interval)
            print()

    except KeyboardInterrupt:
        print("\nProgram interrupted. Saving entries...")
        # Save the seen entries and last ID before exiting
        save_seen_entries(seen_entries, last_id)



if __name__ == '__main__':
    url = 'https://rss.politico.com/congress.xml'
    # Get the extra parameter if provided
    article_count = sys.argv[1] if len(sys.argv) > 1 else None
    monitor_feed(url, count=int(article_count) if article_count else 1)
