import os
import sys
import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🎯 한국 공휴일 (추가 가능)
HOLIDAYS = {
    "2025-01-01", "2025-03-01", "2025-05-05", "2025-05-06", "2025-06-06",
    "2025-08-15", "2025-10-03", "2025-10-06", "2025-10-07", "2025-10-08",
    "2025-10-09", "2025-12-25"
}

# 📆 오늘 날짜
today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")
formatted_date = today.strftime('%m월 %d일')  # 예: 04월 10일

# 🚫 공휴일 제외
if today_str in HOLIDAYS:
    print(f"📢 오늘({today_str})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# ✅ 슬랙 인증
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL") or "#general"  # 기본 채널

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ 슬랙 전송 에러: {e}")

def get_meal_count_message():
    import json

    # 🔹 구글 시트 인증
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # 👉 GitHub Secrets에서 GOOGLE_CREDS_JSON 읽어서 인증하기
    creds_json = os.environ.get("GOOGLE_CREDS_JSON")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # 🔹 스프레드시트 열기
    spreadsheet_id = '1xMd48_CrMeq7WjXxapSNv9YWrDmcLN_0cx-16jidJyg'
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet('식수_25년 03월~04월')

    # 🔹 데이터 읽기
    data = worksheet.get_all_values()
    date_row = data[0]

    # 🔹 오늘 날짜가 포함된 열 찾기
    target_col = None
    for idx, col_val in enumerate(date_row):
        if formatted_date in col_val:
            target_col = idx
            break

    if target_col is not None:
        lunch = data[1][target_col] if len(data) > 1 else 'N/A'
        dinner = data[2][target_col] if len(data) > 2 else 'N/A'
        return f"🍽️ *{formatted_date} 식수 인원 안내*\n- 중식: {lunch}명\n- 석식: {dinner}명"
    else:
        return f"❗ `{formatted_date}` 날짜를 시트에서 찾을 수 없습니다."

def main():
    message = get_meal_count_message()
    send_slack_message(message, SLACK_CHANNEL)

if __name__ == "__main__":
    main()
