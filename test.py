import requests

url = 'https://www.politico.com/rss/politicopicks.xml'


response = requests.get(url)
print(response)