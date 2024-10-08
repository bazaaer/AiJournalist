import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv


load_dotenv()

url = os.getenv('WP_URL')
user = os.getenv('WP_USER')
password = os.getenv('WP_PASSWORD')


def create_post(content, post_title, media_id=None):
    post_endpoint = f"{url}/posts"
    post_data = {
        'title': post_title,
        'content': content,
        'status': 'publish',
    }

    if media_id:
        post_data['featured_media'] = media_id

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(post_endpoint,
                             auth=HTTPBasicAuth(user, password),
                             headers=headers,
                             data=json.dumps(post_data))

    if response.status_code == 201:
        print(f"Post created successfully: {response.json().get('link')}")
    else:
        print(f"Failed to create post (status code {
              response.status_code}): {response.content}")


def upload_image(image_path, image_name, content_type):
    media_endpoint = f"{url}/media"

    with open(f"images/{image_path}", 'rb') as img_file:
        # Correct format for `files` parameter
        files = {'file': (image_name, img_file, content_type)}

        response = requests.post(media_endpoint,
                                 auth=HTTPBasicAuth(user, password),
                                 files=files)

    if response.status_code == 201:
        # Successful upload
        media_id = response.json().get('id')
        print(f"Image uploaded successfully with ID: {media_id}")
        return media_id
    else:
        print(f"Failed to upload image (status code {
              response.status_code}): {response.content}")
        return None
