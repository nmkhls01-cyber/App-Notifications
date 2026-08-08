import requests
import json

# الحسابات المستهدفة
accounts = ["mhnd_Rt", "Drb7h1"]
saved_data = None

for acc in accounts:
    # نستخدم واجهة بديلة وخفيفة تابعة لخدمات الـ RSS المباشرة الموثوقة
    api_url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{acc}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            # استخراج محتوى التغريدة بذكاء من الـ JSON العائد من الموقع الرسمي
            data_json = response.json()
            timeline = data_json.get("timeline", {}).get("instructions", [])
            
            for instruction in timeline:
                entries = instruction.get("addEntries", {}).get("entries", [])
                if not entries:
                    entries = instruction.get("pinEntry", {}).get("entry", [])
                    if entries: entries = [entries]
                
                for entry in entries:
                    content = entry.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                    text = content.get("legacy", {}).get("full_text")
                    tweet_id = content.get("legacy", {}).get("id_str")
                    
                    if text and tweet_id:
                        saved_data = {
                            "text": f"[{acc}]: {text}",
                            "link": f"https://x.com/{acc}/status/{tweet_id}"
                        }
                        break
                if saved_data:
                    break
        if saved_data:
            break
    except Exception as e:
        print(f"Error fetching {acc}: {e}")

# حفظ النتيجة في ملف التطبيق
if saved_data:
    with open("latest_tweet.json", "w", encoding="utf-8") as f:
        json.dump(saved_data, f, ensure_ascii=False)
