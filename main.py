import os
import sys
import datetime
import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2026-01-01",  # 신정
    "2026-02-16",  # 설 연휴
    "2026-02-17",  # 설날
    "2026-02-18",  # 설 연휴
    "2026-03-02",  # 대체공휴일
    "2026-05-05",  # 어린이날
    "2026-05-25",  # 대체공휴일
    "2026-06-03",  # 지방선거
    "2026-08-17",  # 대체공휴일
    "2026-09-24",  # 추석 연휴
    "2026-09-25",  # 추석
    "2026-10-05",  # 대체공휴일
    "2026-10-09",  # 한글날
    "2026-12-25",  # 크리스마스
}

# 📆 오늘 날짜 가져오기
today = datetime.date.today().strftime("%Y-%m-%d")

# 🚫 오늘이 공휴일이면 실행하지 않고 종료
if today in HOLIDAYS:
    print(f"📢 오늘({today})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 환경 변수에서 Slack 토큰 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f":loudspeaker: *『인사총무팀 공지』* \n\n"

        notice_msg = (
            f"안녕하세요? 평택 클러스터 구성원 여러분! 인사총무팀 입니다. :blush:\n"
            f"\n"
            f":지게차:*지게차 관련 사항*:지게차2: 을 아래와 같이 공지 드리오니 협조 부탁드리겠습니다.\n\n"
            f"\n"
            f":체크1: *<지게차 A/S 양식>*\n\n"
            f":one: *이름* : 김컬리\n"
            f":two: *부서* : 인사총무팀 총무/시설\n"
            f":three: *장비* : 카운터 / 리치 / EPT _ 각 장비 번호\n"
            f":four: *장소* : 현재 A/S 필요 장비의 위치를 기입\n"
            f":five: *증상* : 현재 A/S 필요 장비의 증상 상세하게 설명 _ 사진 첨부 필수\n"
            f"\n\n"
            f":alert: *<중요사항>* :alert: \n"
            f"> 스마트랙 핀번호를 입력 하는 기기는 *핀번호 입력 외 임의 조작,과도하게 꺽음 등 행동 절대 금지*\n"
            f"\n\n"
            f"📌 지게차 핀번호 관련사항은 EHS_평택 담당자분들께 문의 부탁드립니다.\n"
            f"📌 지게차 A/S의 경우 평일에만 진행되며, 주말 및 공휴일의 경우 휴무입니다.\n"
            f"\n\n"
            f":slack: *<문의사항>* :*<@U05NXEAL43E> <@U04RT8X7D9N> <@U07QC9WQ8JX>*\n\n"
            f"감사합니다.\n"
       )
 
        # 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
