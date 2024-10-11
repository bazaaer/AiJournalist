# AI Journalist

## Description

This project is a couple of python scripts that work together to generate a news article based on the output of a rss (feed)[]. The project is divided into two main parts:

- The first part is the `api.py` script. This script contains all the functions and prompt engineering for calling the chatgpt api.
- The second part is the `upload.py` script. This script contains functions to upload the generated article to the hosted wordpress website.
- The `main.py` script fetches a set amount of recent articles from the rss feed and checks if they are in the `generated_articles.json` file. If they are not, it generates an image that is politically neutral and a news article based on the article's content. The article is then saved in the `generated_articles.json` file.

The project is then ran as main.py. Which keeps checking if the rss feed has new articles and if it does, it generates an article and uploads it to the website.

## Installation

To install the project, you need to have python installed. You can download it from [here](https://www.python.org/downloads/). After installing python, you need to install the required packages. You can do this by running the following command in the terminal:

```bash
git clone https://github.com/bazaaer/AiJournalist
```

While in the root of the project, run the following command in the terminal:

```bash
pip install -r requirements.txt
```

## Usage

To use the project, you need to have a hosted wordpress website. You need to have the following environment variables in a `.env` file in the root of the project:

```env
WORDPRESS_URL=<your-wordpress-url>
WORDPRESS_USERNAME=<your-wordpress-username>
WORDPRESS_PASSWORD=<your-wordpress-password>
OPENAI_API_KEY=<your-openai-api-key>
```

After setting up the environment variables, you can run the project by running the following command in the terminal:

```bash
python main.py [article_count] [noimg/aiimg/webimg]
```
Article count is a parameter to set how many articles the feedparser function fetches at once. Usefull for catching up in articles if the application was down. Default=1 --> fetches only the most recent article.
