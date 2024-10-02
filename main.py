import time
import re
import json
import os
from datetime import datetime
import requests
import feedparser

from api import generate_new_image, genererate_neutral_prompt, check_article_relevance, generate_new_article


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


def write_article_to_file(article_id, ai_article, image_prompt, ai_image_url, file_path):
    # Create a dictionary with the article details
    article_data = {
        'id': article_id,
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


def monitor_feed(feed_url, interval=10, genertate_image=True):
    seen_entries, last_id = load_seen_entries()

    try:
        while True:
            # Call the updated get_latest_news to get a list of articles
            news_items = get_latest_news(feed_url)

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
                        ai_article = generate_new_article(response['input_article'])
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
                            last_id, ai_article, neutral_prompt, ai_image_url, "generated_articles.json")
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
    monitor_feed('https://rss.politico.com/congress.xml')
