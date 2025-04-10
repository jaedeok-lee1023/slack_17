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
formatted_date = today.strftime('%-m월 %-d일')

print(f"[INFO] 오늘 날짜: {formatted_date}")

# 🚫 공휴일 체크
if today_str in HOLIDAYS:
    print(f"📢 오늘({today_str})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 🔐 환경 변수 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL") or "#general"

if not SLACK_TOKEN:
    print("❌ SLACK_TOKEN 환경 변수가 비어 있습니다.")
    sys.exit(1)

print("[INFO] 슬랙 토큰, 채널 로드 완료")

# 📤 슬랙 메시지 전송 함수
def send_slack_message(message):
    print("[INFO] 슬랙 메시지 전송 중...")
    try:
        client = WebClient(token=SLACK_TOKEN)
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        print(f"[SUCCESS] 슬랙 메시지 전송 완료: {response['ts']}")
    except SlackApiError as e:
        print(f"⚠️ 슬랙 전송 에러: {e.response['error']}")

# 📊 스프레드시트에서 식수 인원 가져오기
def get_meal_count_message():
    csv_url = "https://docs.google.com/spreadsheets/d/19YaBfbuX2PGdwso0iyVan0kd2G7wB0DE/export?format=csv&gid=1938075870"
    print(f"[INFO] CSV 데이터 요청 중... URL: {csv_url}")
    
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ 스프레드시트 요청 실패: {e}")
        sys.exit(1)

    response.encoding = "utf-8"
    rows = list(csv.reader(response.text.splitlines()))

    print(f"[INFO] 시트에서 {len(rows)}줄 로드됨")

    if len(rows) < 3:
        print("❌ 데이터가 부족합니다 (헤더, 중식, 석식 필요)")
        sys.exit(1)

    header = rows[0]
    lunch_row = rows[1]
    dinner_row = rows[2]

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
        print(f"❗ `{formatted_date}` 날짜를 시트에서 찾을 수 없습니다.")
        return f"❗ `{formatted_date}` 날짜를 시트에서 찾을 수 없습니다."

# 🏃 메인 실행
def main():
    print("[INFO] 프로그램 시작")
    message = get_meal_count_message()
    print(f"[INFO] 메시지 생성 완료:\n{message}")
    send_slack_message(message)

if __name__ == "__main__":
    print("✅ [START] 코드 실행됨")  # ← 여기에 추가!
    main()
