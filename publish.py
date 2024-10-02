import requests
from requests.auth import HTTPBasicAuth
import json

# Wordpress site URL and credentials from .env file
from dotenv import load_dotenv
import os
load_dotenv()

url = os.getenv('WP_URL')
user = os.getenv('WP_USER')
password = os.getenv('WP_PASSWORD')

# Get the token
auth = HTTPBasicAuth(user, password)
response = requests.post(url + '/wp-json/jwt-auth/v1/token', auth=auth)
data = response.json()
token = data['token']

# Get the posts
response = requests.get(url + '/wp-json/wp/v2/posts')
posts = response.json()

# Publish the posts
for post in posts:
    response = requests.post(url + '/wp-json/wp/v2/posts/' + str(post['id']), headers
    = {'Authorization': 'Bearer ' + token}, json={'status': 'publish'})
    
    print(response.json())