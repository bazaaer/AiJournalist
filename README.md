<div align="center">
<pre>
  ___  _____     ___                              _ _     _   
 / _ \|_   _|   |_  |                            | (_)   | |  
/ /_\ \ | |       | | ___  _   _ _ __ _ __   __ _| |_ ___| |_ 
|  _  | | |       | |/ _ \| | | | '__| '_ \ / _` | | / __| __|
| | | |_| |_  /\__/ / (_) | |_| | |  | | | | (_| | | \__ \ |_ 
\_| |_/\___/  \____/ \___/ \__,_|_|  |_| |_|\__,_|_|_|___/\__|
                                                              
                                              
----
This project is a couple of python scripts that work together to generate a news article based on the output of a rss (feed). 
</pre>
</div>

## Table of contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributors](#contributors)
- [Thanks](#thanks)

## Description

This project is a couple of python scripts that work together to generate a news article based on the output of a rss (feed)[]. The project is divided into two main parts:

- The first part is the `api.py` script. This script contains all the functions and prompt engineering for calling the chatgpt api.
- The second part is the `upload.py` script. This script contains functions to upload the generated article to the hosted wordpress website.
- The `main.py` script fetches a set amount of recent articles from the rss feed and checks if they are in the `mongo database`. If they are not, it generates an image that is politically neutral and a news article based on the article's content. The article is then saved in the `mongo database` file.

The project is then ran as main.py. Which keeps checking if the rss feed has new articles and if it does, it generates an article and uploads it to the website.

## Installation

To install the project, you need docker and docker-compose installed on your machine. You can install docker and docker-compose by following the instructions on the [official docker website](https://docs.docker.com/get-docker/).

```bash
git clone https://github.com/bazaaer/AiJournalist
```

Navigate to the .devcontainer folder and create a .env file with the following content (Fill this with our own data):

```env
WP_URL=https://yourWPdomain.com/wp-json/wp/v2 # IMPORTANT: add /wp-json/wp/v2 at the end of your WP URL
WP_USER=username
WP_PASSWORD="password"
PYTHONUNBUFFERED=1
MONGO_USER=root
MONGO_PASSWORD=examplepassword
MONGO_HOST=mongodb
MONGO_PORT=27017
REDIS_HOST=redis
REDIS_PORT=6379
```

Now you can open the project in a devcontainer. In visual studio code, you can do this by pressing `F1` and typing `Remote-Containers: Open Folder in Container...`. Then select the folder where you cloned the project. Or `Reopen in Container` if you already have the project open.


## Usage

To run the project, you need to run the following command in the terminal:

```bash
python main.py [article_count] [noimg/aiimg/webimg]
```

Article count is a parameter to set how many articles the feedparser function fetches at once. Usefull for catching up in articles if the application was down. By default this is set to 1. wich will fetch the most recent article.

## Dependencies

- python:1-3.12-bullseye [![Python: 1.3.12](https://img.shields.io/badge/Python-3.12.bullseye-green)](https://hub.docker.com/layers/library/python/3.12-bullseye/images/sha256-c820d5e7133d9017e324fc31988e243dca9f4e72721733c34f86b46b340aa5b7?context=explore)
- - Python dependencies can be found in the requirements.txt file.
- mongo:6 [![Mongo: 6](https://img.shields.io/badge/Mongo-6-green)](https://hub.docker.com/layers/library/mongo/6/images/sha256-7b3b3b3b1)
- redis:6 [![Redis: 6](https://img.shields.io/badge/Redis-6-green)](https://hub.docker.com/layers/library/redis/6/images/sha256-7b3b3b3b1)

## Contributors

@bazaaer
@vinniepost

## Thanks

This project was made under the supervision of @hascodi. Thanks for the help and guidance.
