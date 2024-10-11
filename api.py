from io import BytesIO
from PIL import Image
import requests
from datetime import datetime
import os
import json
from openai import OpenAI
client = OpenAI()


def generate_new_image(prompt, title):
    """Generate a new image using the DALL-E-3 model and save it to the 'images' directory.

    Args:
        prompt (str): The prompt to generate the image.
        title (str): Title for the image to be saved.

    Returns:
       image_url (str): Link where the image is hosted, available for half an hour after creation.
    """
    # Generate the image
    ai_image = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1,
    )
    image_url = ai_image.data[0].url
    print(f"Image generated successfully. URL: {image_url}")

    # Directory where images will be saved
    image_directory = "temp_images"

    # Create directory if it doesn't exist
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    # Generate a unique image filename
    formatted_title = title.lower().replace(" ", "_")
    image_filename = f"{image_directory}/image_{formatted_title}.webp"

    # Download the image
    response = requests.get(image_url)

    # Save the image with compression
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        # Compress and save the image as WEBP with quality 85 (you can adjust the value)
        img.save(image_filename, "WEBP", quality=85)
        print(f"Compressed image saved successfully as {image_filename}.")
    else:
        print("Failed to download image.")

    return image_url


def genererate_neutral_prompt(prompt):
    """Generates a neutral prompt from a given prompt. The neutral prompt is needed to generate images using the DALL-E-3 model.

    Args:
        prompt (_str_): A given prompt to generate a neutral prompt from.

    Returns:
        neutral_promt: The neutral prompt
    """
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
    """Checks if the given article is relevant to the presidential election.

    Args:
        article (_type_): article to check for relevance to the presidential election.

    Returns:
        (bool?) _type_: returns True if the article is relevant to the presidential election, otherwise False.
    """

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


def apply_tags(article):
    """Apply tags to the given article.

    Args:
        article: article to apply tags to.

    Returns:
        a list of tags
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "choose_tags",
                "description": "The model needs to choose tags from a list to apply to an article",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tags": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "-",
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
                                    "War"
                                ]
                            }
                        }
                    },
                    "required": ["tags"],
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
    """Generate a new article based on the given article.

    Args:
        article (_type_): An article to generate a new article from.

    Returns:
        article: The rewritten article.
    """
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
    """Generates a new title for the given article.

    Args:
        title (str): The original title of the article.
        article (): edited article to generate a new title from.

    Returns:
        str : Generated title for the article.
    """
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

def generate_web_search(title, article):
    """Generates a web search for an image based on the given article title."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract full names from the article. If there are multiple name, separate them by 'and' and only pick the 2 most important names. If the article contains no full names, decribe the article in 1 scentence: "
            },
            {
                "role": "user",
                "content": f"{title}\n\n{article}"
            }
        ]
    )
    print("GENERATED" + response.choices[0].message.content)
    return response.choices[0].message.content