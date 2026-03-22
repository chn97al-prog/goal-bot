import requests
import time
send_message("✅ البوت شغال")
BOT_TOKEN = "YOUR_TOKEN"
CHAT_ID = "@your_channel"

matches_messages = {}
last_scores = {}

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })
    return res.json()["result"]["message_id"]

def edit_message(message_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "text": text
    })

def get_matches():
    url = "https://site.api.espn.com/apis/v2/sports/soccer/eng.1/scoreboard"
    data = requests.get(url).json()
    return data["events"]

while True:
    try:
        matches = get_matches()

        for m in matches:
            match_id = m["id"]

            comp = m["competitions"][0]
            home = comp["competitors"][0]["team"]["name"]
            away = comp["competitors"][1]["team"]["name"]

            home_score = int(comp["competitors"][0]["score"])
            away_score = int(comp["competitors"][1]["score"])

            status = m["status"]["type"]["description"]

            current_score = f"{home_score}-{away_score}"

            # 🟢 البوست الرئيسي
            main_text = f"""
🏟 {home} vs {away}
📊 {home_score} - {away_score}
⏱ {status}
"""

            # أول مرة
            if match_id not in matches_messages:
                msg_id = send_message(main_text)
                matches_messages[match_id] = msg_id
                last_scores[match_id] = current_score
            else:
                # تحديث البوست
                edit_message(matches_messages[match_id], main_text)

                # ⚽ كشف الهدف
                if last_scores[match_id] != current_score:
                    
                    # تحديد من سجل
                    old_home, old_away = map(int, last_scores[match_id].split("-"))

                    if home_score > old_home:
                        scorer = home
                    elif away_score > old_away:
                        scorer = away
                    else:
                        scorer = "هدف"

                    goal_text = f"""
🚨 GOAL!
⚽ {scorer} يسجل
📊 {home_score} - {away_score}
"""

                    send_message(goal_text)

                    last_scores[match_id] = current_score

        time.sleep(5)

    except Exception as e:
        print(e)
        time.sleep(5)
