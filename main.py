import feedparser
import time
import re
import json
import os
import atexit

def save_seen_entries(seen_entries, last_id):
    with open('seen_entries.json', 'w') as f:
        json.dump({'last_id': last_id, 'entries': seen_entries}, f)

def load_seen_entries():
    if os.path.exists('seen_entries.json'):
        with open('seen_entries.json', 'r') as f:
            data = json.load(f)
            return data['entries'], data['last_id']
    return [], 0  # Return empty list and ID 0 if file doesn't exist

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

def get_latest_news(feed_url, count=1):
    feed = feedparser.parse(feed_url)
    title = None
    link = None
    published = None
    content = None

    for entry in feed.entries[:count]:
        title = entry.title
        link= entry.link
        published = entry.published
        if hasattr(entry, 'content'):
            content = entry.content[0].value
            content = remove_html_tags(content)
        print()
    return title, link, published, content


def monitor_feed(feed_url, interval=10):
    seen_entries, last_id = load_seen_entries()
    
    try:
        while True:
            # Your function logic here
            title, link, published, content = get_latest_news(feed_url)
            new_entry = {'id': last_id + 1, 'title': title, 'link': link, 'published': published, 'content': content}

            if not entry_exists(seen_entries, new_entry):
                last_id += 1
                seen_entries.append(new_entry)
                print(f"New article found: {title}")
                print(new_entry['content'])
                ai_article = generate_new_article(new_entry['content'])


                # Register the cleanup function
                atexit.register(save_seen_entries, seen_entries, last_id)



            else:
                print("No new article found.")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nProgram interrupted. Saving entries...")
        # Optionally, you can call save_seen_entries here explicitly
        save_seen_entries(seen_entries, last_id)


def generate_new_article(article):
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
        {"role": "system", "content": "You are a journalist writing an article for a major news outlet in Belguim for Dutch speakers. Your editor has asked you to rerwrite the following article about United States congress. The article should be written so that it is easy to understand for a general audience. Explain difficult concepts/terminololy. Base your resopnse ONLY on the following article: "},
        {
            "role": "user",
            "content": {article}
        }
        ]
    )


    

# Replace with your actual feed URL
monitor_feed('https://rss.politico.com/congress.xml')