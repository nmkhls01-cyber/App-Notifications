import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# قائمة الحسابات المراد مراقبتها
accounts = ["Drb7h1", "mhnd_Rt"]
headers = {'User-Agent': 'Mozilla/5.0'}

latest_tweets = []

for acc in accounts:
    url = f"https://nitter.poast.org/{acc}/rss"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            item = soup.find("item")
            if item:
                text = item.title.text if item.title else "تغريدة جديدة"
                link = item.link.text if item.link else f"https://x.com/{acc}"
                pub_date = item.pubDate.text if item.pubDate else ""
                
                # حفظ الحساب وتفاصيل التغريدة
                latest_tweets.append({
                    "text": f"[{acc}]: {text}",
                    "link": link,
                    "date": pub_date
                })
    except Exception as e:
        print(f"Error for {acc}: {e}")

# حفظ أحدث تغريدة تم جلبها
if latest_tweets:
    data = {
        "text": latest_tweets[0]["text"],
        "link": latest_tweets[0]["link"]
    }
    with open("latest_tweet.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
