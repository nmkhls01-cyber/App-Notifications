import requests
import json
from bs4 import BeautifulSoup
import email.utils

# الحسابات التي نراقبها
accounts = ["Drb7h1", "mhnd_Rt"]
headers = {'User-Agent': 'Mozilla/5.0'}

latest_tweets = []

for acc in accounts:
    url = f"https://nitter.poast.org/{acc}/rss"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # استخدام xml لقراءة تغذية RSS بشكل أصح
            soup = BeautifulSoup(response.content, "xml")
            item = soup.find("item")
            if item:
                text = item.title.text if item.title else "تغريدة جديدة"
                link = item.link.text if item.link else f"https://x.com/{acc}"
                pub_date_str = item.pubDate.text if item.pubDate else ""
                
                # تحويل تاريخ التغريدة إلى رقم زمني للمقارنة
                try:
                    dt = email.utils.parsedate_to_datetime(pub_date_str).timestamp()
                except:
                    dt = 0
                    
                if dt > 0:
                    latest_tweets.append({
                        "text": f"[{acc}] {text}",
                        "link": link,
                        "time": dt
                    })
    except Exception as e:
        print(f"Error for {acc}: {e}")

# إذا وجدنا تغريدات، نقوم بترتيبها من الأحدث إلى الأقدم
if latest_tweets:
    # فرز التغريدات بناءً على الوقت (الأحدث أولاً)
    latest_tweets.sort(key=lambda x: x["time"], reverse=True)
    
    # حفظ التغريدة الأحدث فقط
    data = {
        "text": latest_tweets[0]["text"],
        "link": latest_tweets[0]["link"]
    }
    with open("latest_tweet.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
