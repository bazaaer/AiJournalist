import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv


load_dotenv()

url = os.getenv('WP_URL')
user = os.getenv('WP_USER')
password = os.getenv('WP_PASSWORD')

allowed_tags = ["-",
                "Biden",
                "Trump",
                "Harris",
                "Biden-Harris",
                "Alabama",
                "Alaska",
                "Arizona",
                "Arkansas",
                "California",
                "Colorado",
                "Connecticut",
                "Delaware",
                "Florida",
                "Georgia",
                "Hawaii",
                "Idaho",
                "Illinois",
                "Indiana",
                "Iowa",
                "Kansas",
                "Kentucky",
                "Louisiana",
                "Maine",
                "Maryland",
                "Massachusetts",
                "Michigan",
                "Minnesota",
                "Mississippi",
                "Missouri",
                "Montana",
                "Nebraska",
                "Nevada",
                "New Hampshire",
                "New Jersey",
                "New Mexico",
                "New York",
                "North Carolina",
                "North Dakota",
                "Ohio",
                "Oklahoma",
                "Oregon",
                "Pennsylvania",
                "Rhode Island",
                "South Carolina",
                "South Dakota",
                "Tennessee",
                "Texas",
                "Utah",
                "Vermont",
                "Virginia",
                "Washington",
                "West Virginia",
                "Wisconsin",
                "Wyoming",
                "Washington D.C.",
                "Puerto Rico",
                "Guam",
                "U.S. Virgin Islands",
                "American Samoa",
                "Northern Mariana Islands",
                "Senate",
                "House",
                "Congress",
                "Supreme Court",
                "White House",
                "Capitol",
                "Democrat",
                "Republican",
                "Independent",
                "Libertarian",
                "Green Party",
                "Constitution Party",
                "Foreign News",
                "War"]


def get_tag_id(tag_name):
    tag_endpoint = f"{url}/tags"
    headers = {
        'Content-Type': 'application/json',
    }
    params = {'search': tag_name}

    # Check if the tag exists
    response = requests.get(
        tag_endpoint,
        auth=HTTPBasicAuth(user, password),
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        tags = response.json()
        if tags:
            # If the tag exists, return its ID
            return tags[0]['id']
        else:
            print(f"Tag '{tag_name}' does not exist.")
    else:
        print(f"Failed to retrieve tag '{tag_name}' (status code {
              response.status_code}): {response.content}")

    return None


def create_post(content, post_title, media_id=None, tags='-'):
    tags = tags['tags']

    tag_ids = [get_tag_id(tag) for tag in tags if get_tag_id(tag) is not None]

    post_endpoint = f"{url}/posts"
    post_data = {
        'title': post_title,
        'content': content,
        'status': 'publish',
        'tags': tag_ids,
        'categories': [79]
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

    with open(f"temp_images/{image_path}", 'rb') as img_file:
        # Correct format for `files` parameter
        files = {'file': (image_name, img_file, content_type)}

        response = requests.post(media_endpoint,
                                 auth=HTTPBasicAuth(user, password),
                                 files=files)

    if response.status_code == 201:
        # Successful upload
        media_id = response.json().get('id')
        print(f"Image uploaded successfully with ID: {media_id}")
        os.remove(f'temp_images/{image_path}')
        print(f"Image deleted: {image_path}")
        return media_id
    else:
        print(f"Failed to upload image (status code {
              response.status_code}): {response.content}")
        return None
