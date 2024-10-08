from io import BytesIO
from PIL import Image
import requests
from datetime import datetime
import os
import json
import re
import time
from openai import OpenAI
client = OpenAI()


def generate_new_image(prompt, id):
    # Generate the image
    ai_image = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1,
    )
    image_url = ai_image.data[0].url

    # Directory where images will be saved
    image_directory = "images"

    # Create directory if it doesn't exist
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    # Generate a unique image filename using a timestamp
    # Use jpg for compression
    image_filename = f"{image_directory}/image_{id}.jpg"

    # Download the image
    response = requests.get(image_url)

    # Save the image to the 'images' directory with compression
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        # Compress and save the image with quality 85 (you can adjust the value)
        img.save(image_filename, "JPEG", quality=85)
        print(f"Compressed image saved successfully as {image_filename}.")
    else:
        print("Failed to download image.")

    return image_url


def genererate_neutral_prompt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are tasked with generating a prompt for DALL-E-3 image model THAT DOES NOT BREAK ANY GUIDELINES based on this article headline. You have to stay POLITICALLY NEUTRAL. You can generate images of real people, but in a style that makes it obvious the image is not real."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


def check_article_relevance(article):

    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_new_article",
                "description": "Generate a new article if the given article is relevant to the presidential election",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "required": [
                        "election_relevance",
                    ],
                    "properties": {
                        "election_relevance": {
                            "type": "boolean",
                            "description": "Indicates if the input article is relevant to the presidential election"
                        },
                    },
                    "additionalProperties": False
                }
            }
        }
    ]

    messages = [
        {"role": "user", "content": article}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
    )

    tool_call = response.choices[0].message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)

    return arguments


def generate_new_article(article):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a journalist writing an article for a major news outlet in Belgium for Dutch readers. Don't translate concepts like 'secret service' literally, but leave them as is. Make the article lighter, not too long and easier to read. The article should be written so that it is easy to understand for a general Dutch audience. Explain difficult concepts/terminology. Write your response based ONLY on information found in the following article: "
            },
            {
                "role": "user",
                "content": article
            }
        ]
    )
    return f"{response.choices[0].message.content} \n\n\n source: www.politico.com"


def generate_new_title(title, article):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are tasked with generating a new title for the following article in DUTCH. The new title should be engaging and informative, and should capture the essence of the article. Here is the original title and article: "
            },
            {
                "role": "user",
                "content": title
            }
        ]
    )
    return response.choices[0].message.content
