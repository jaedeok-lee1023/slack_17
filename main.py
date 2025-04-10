import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import requests
import re

def main():
    today = datetime.datetime.today().strftime('%m월 %d일')

    # 🔹 URL → spreadsheet ID 추출
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1xMd48_CrMeq7WjXxapSNv9YWrDmcLN_0cx-16jidJyg/edit?gid=414313191'
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', spreadsheet_url)
    spreadsheet_id = match.group(1) if match else None
    if not spreadsheet_id:
        raise ValueError("❗ 스프레드시트 ID 추출 실패")

    # 🔹 인증
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
    client = gspread.authorize(creds)

    # 🔹 시트 열기
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet('식수_25년 03월~04월')

    # 🔹 데이터 가져오기
    data = worksheet.get_all_values()
    date_row = data[0]
    target_col = None
    for idx, col_val in enumerate(date_row):
        if today in col_val:
            target_col = idx
            break

    if target_col is not None:
        lunch = data[1][target_col] if len(data) > 1 else 'N/A'
        dinner = data[2][target_col] if len(data) > 2 else 'N/A'
        message = f"🍽️ *{today} 식수 인원 안내*\n- 중식: {lunch}명\n- 석식: {dinner}명"
    else:
        message = f"❗ 스프레드시트에서 `{today}` 날짜를 찾을 수 없습니다."

    # 🔹 슬랙 전송
    webhook_url = 'https://hooks.slack.com/services/XXX/YYY/ZZZ'
    requests.post(webhook_url, json={"text": message})

if __name__ == "__main__":
    main()
