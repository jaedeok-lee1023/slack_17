import os
import sys
import datetime
import requests
import csv
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 🎯 한국 공휴일
HOLIDAYS = {
    "2025-01-01", "2025-03-01", "2025-05-05", "2025-05-06", "2025-06-06",
    "2025-08-15", "2025-10-03", "2025-10-06", "2025-10-07", "2025-10-08",
    "2025-10-09", "2025-12-25"
}

# 📅 오늘 날짜
today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")
formatted_date = today.strftime('%m월 %d일')  # 예: 04월 10일

# 🚫 공휴일 체크
if today_str in HOLIDAYS:
    print(f"📢 오늘({today_str})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 🔐 환경 변수 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL") or "#general"

# 📤 슬랙 메시지 전송 함수
def send_slack_message(message):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
    except SlackApiError as e:
        print(f"⚠️ 슬랙 전송 에러: {e}")

# 📊 스프레드시트에서 식수 인원 가져오기
def get_meal_count_message():
    csv_url = "https://docs.google.com/spreadsheets/d/13al3WiKqEEQKN-UofBq_wzmcWSKte0ptWSC79kWFO_w/export?format=csv&gid=1135001380"
    response = requests.get(csv_url)
    response.encoding = "utf-8"

    rows = list(csv.reader(response.text.splitlines()))

    # 첫 줄은 날짜가 들어 있는 열
    header = rows[0]
    lunch_row = rows[1]
    dinner_row = rows[2]

    # 오늘 날짜에 해당하는 열 찾기
    target_col = None
    for idx, col in enumerate(header):
        if formatted_date in col:
            target_col = idx
            break

    if target_col is not None:
        lunch = lunch_row[target_col] if len(lunch_row) > target_col else "N/A"
        dinner = dinner_row[target_col] if len(dinner_row) > target_col else "N/A"
        return f"🍽️ *{formatted_date} 식수 인원 안내*\n- 중식: {lunch}명\n- 석식: {dinner}명"
    else:
        return f"❗ `{formatted_date}` 날짜를 시트에서 찾을 수 없습니다."

# 🏃 메인 실행
def main():
    message = get_meal_count_message()
    send_slack_message(message)

if __name__ == "__main__":
    main()
