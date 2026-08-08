import requests
import json
from bs4 import BeautifulSoup

# الحسابات المراد مراقبتها (الأول ثم الثاني)
accounts = ["mhnd_Rt", "Drb7h1"]
headers = {'User-Agent': 'Mozilla/5.0'}

saved_data = None

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
                
                saved_data = {
                    "text": f"[{acc}]: {text}",
                    "link": link
                }
                break # أول ما يجد تغريدة لأي منهما يعتمدها فوراً
    except Exception as e:
        print(f"Error for {acc}: {e}")

# حفظ البيانات في الملف
if saved_data:
    with open("latest_tweet.json", "w", encoding="utf-8") as f:
        json.dump(saved_data, f, ensure_ascii=False)
