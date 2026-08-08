import requests
import json
from bs4 import BeautifulSoup

url = "https://nitter.poast.org/Drb7h1/rss"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        item = soup.find("item")
        if item:
            text = item.title.text if item.title else "تغريدة جديدة"
            link = item.link.text if item.link else "https://x.com/Drb7h1"
            
            data = {"text": text, "link": link}
            with open("latest_tweet.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
except Exception as e:
    print(f"Error: {e}")
