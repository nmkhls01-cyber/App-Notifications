import requests, json
from bs4 import BeautifulSoup

url = "https://nitter.poast.org/Drb7h1/rss"
r = requests.get(url)
soup = BeautifulSoup(r.content, "xml")
item = soup.find_all("item")[0]

data = {"text": item.title.text, "link": item.link.text}
with open("latest_tweet.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
