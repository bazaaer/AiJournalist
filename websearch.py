import requests
import os
import urllib.request

def download_image(query, image_name="image"):
    # Create a directory to save images
    if not os.path.exists("downloaded_images"):
        os.makedirs("downloaded_images")

    # Your Bing Search API key
    api_key = "d28f6a17c7b442878b08f8c50d4b4e69"
    endpoint = "https://api.bing.microsoft.com/v7.0/images/search"

    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 1}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        # Extract the first image URL and download it
        img = results.get("value", [])[0]
        img_url = img["contentUrl"]
        try:
            # Use the provided image_name parameter to name the image
            img_path = f"downloaded_images/{image_name}.jpg"
            urllib.request.urlretrieve(img_url, img_path)
            print(f"Downloaded image: {img_url}")
        except Exception as e:
            print(f"Error downloading image: {e}")

    except Exception as e:
        print(f"Failed to retrieve images from Bing: {e}")

# Replace 'YOUR_QUERY' with the prompt you want to search for
download_image("duck", image_name="duck_image")
