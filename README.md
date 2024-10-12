<div align="center">
<pre>
  ___  _____     ___                              _ _     _   
 / _ \|_   _|   |_  |                            | (_)   | |  
/ /_\ \ | |       | | ___  _   _ _ __ _ __   __ _| |_ ___| |_ 
|  _  | | |       | |/ _ \| | | | '__| '_ \ / _` | | / __| __|
| | | |_| |_  /\__/ / (_) | |_| | |  | | | | (_| | | \__ \ |_ 
\_| |_/\___/  \____/ \___/ \__,_|_|  |_| |_|\__,_|_|_|___/\__|
                                                              
[![Python: 1.3.12](https://img.shields.io/badge/Python-3.12.bullseye-blue)](https://hub.docker.com/layers/library/python/3.12-bullseye/images/sha256-c820d5e7133d9017e324fc31988e243dca9f4e72721733c34f86b46b340aa5b7?context=explore) [![Mongo: 6](https://img.shields.io/badge/Mongo-6-green)](https://hub.docker.com/layers/library/mongo/6/images/sha256-7b3b3b3b1) [![Redis: 6](https://img.shields.io/badge/Redis-6-red)](https://hub.docker.com/layers/library/redis/6/images/sha256-7b3b3b3b1)
----
This project is a couple of python scripts that work together to generate
a news article based on the output of a rss (feed). 
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

## Installation (to edit the project)

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


## Usage (to run the project)

### Downloading the project

To download the project, you need to run the following command in the terminal:

```bash
git clone 
```

Once you have downloaded the project, you need to navigate to the project folder and add the following environment variables to the `.env` file:
(Don't forget to fill in the variables with your own data)

```env
WP_URL=https://< YOUR WORDPRESS URL >/wp-json/wp/v2
WP_USER=<WORDPRESS USER >
WP_PASSWORD=<WORDPRESS PASSWORD (API KEY)>
OPENAI_API_KEY=<OPENAI API
BING_API_KEY=<BING API KEY>
MONGO_USER=<MONGO USER>
MONGO_PASSWORD=<MONGO PASSWORD>
MONGO_HOST=mongodb
MONGO_PORT=27017
REDIS_HOST=redis
REDIS_PORT=6379
COUNT=2 (Amount of articles to backlog)
IMG_OPTION= (Options: webimg/aiimg/noimg)
```

### Running the project

To run the project, you need to run the following command in the terminal:

When on linux: 

```bash
bash run.sh
```

When on windows:

```bash
run.bat
```

### Adding new tags

To add a new tag you will need to create it via wordpress. After that you can add the tag to the `tags` list in the `api.py` script around line 160.

## Dependencies

- python:1-3.12-bullseye 
- - Python dependencies can be found in the requirements.txt file.
- mongo:6 
- redis:6 

## Contributors

@bazaaer
@vinniepost

## Thanks

This project was made under the supervision of @hascodi. Thanks for the help and guidance.
