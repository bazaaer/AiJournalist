import requests
import os
from dotenv import load_dotenv
from PIL import Image
import urllib.request
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

def search_web_image(query, title):
    # Create a directory to save images
    if not os.path.exists("temp_images"):
        os.makedirs("temp_images")

    # Get the Bing API key from the environment variables
    BING_API_KEY = os.getenv("BING_API_KEY")
    endpoint = "https://api.bing.microsoft.com/v7.0/images/search"

    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": query, "count": 1}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        # Extract the first image URL and download it
        img = results.get("value", [])[0]
        img_url = img["contentUrl"]
        try:
            # Download the image as bytes
            img_data = urllib.request.urlopen(img_url).read()

            # Open the image using PIL and convert it to WebP
            image = Image.open(BytesIO(img_data))
            img_path = f"temp_images/image_{title.lower().replace(' ', '_')}.webp"
            image.save(img_path, "WEBP")
            
            print(f"Downloaded and converted image to WebP: {img_path}")
        except Exception as e:
            print(f"Error downloading or converting image: {e}")

    except Exception as e:
        print(f"Failed to retrieve images from Bing: {e}")