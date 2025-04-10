import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import requests

# 🔹 날짜 포맷 (오늘 날짜를 '04월 10일' 형태로 포맷)
today = datetime.datetime.today().strftime('%m월 %d일')  # 예: 04월 10일

# 🔹 구글 스프레드시트 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
client = gspread.authorize(creds)

# 🔹 시트 열기
sheet = client.open_by_key(spreadsheet_id)
worksheet = sheet.worksheet('식수_25년 03월~04월')

# 🔹 시트 전체 데이터 읽기
data = worksheet.get_all_values()

# 🔹 날짜가 있는 열 찾기 (1행 기준)
date_row = data[0]
target_col = None
for idx, col_val in enumerate(date_row):
    if today in col_val:
        target_col = idx
        break

# 🔹 인원 가져오기
if target_col is not None:
    lunch = data[1][target_col] if len(data) > 1 else 'N/A'
    dinner = data[2][target_col] if len(data) > 2 else 'N/A'

    message = f"🍽️ *{today} 식수 인원 안내*\n- 중식: {lunch}명\n- 석식: {dinner}명"
else:
    message = f"❗ 스프레드시트에서 `{today}` 날짜를 찾을 수 없습니다."

# 🔹 Slack으로 전송
webhook_url = 'https://hooks.slack.com/services/XXX/YYY/ZZZ'
requests.post(webhook_url, json={"text": message})
 
        # 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
