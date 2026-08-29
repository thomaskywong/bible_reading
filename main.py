import os
import requests
from bs4 import BeautifulSoup
import datetime as dt
from zoneinfo import ZoneInfo

# Read directly from system environment variables (populated by GitHub Secrets)
PUSHOVER_USER = os.environ.get('PUSHOVER_USER')
PUSHOVER_TOKEN = os.environ.get('PUSHOVER_TOKEN')

if not PUSHOVER_USER or not PUSHOVER_TOKEN:
    raise RuntimeError(
        'Missing PUSHOVER_USER or PUSHOVER_TOKEN in environment variables')


def send_pushover_message(message):
    url = 'https://api.pushover.net/1/messages.json'
    data = {
        'token': PUSHOVER_TOKEN,
        'user': PUSHOVER_USER,
        'message': message
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def main():
    url = 'https://ccfellow.org/Common/Reader/Channel/ShowPage.jsp?Cid=10&Pid=1&Version=0&Charset=big5_hkscs&page=0'

    response = BeautifulSoup(requests.get(url).text, 'html.parser')

    title_cells = response.find_all('td', class_='devotiontxtbold2')
    title_zh = title_cells[0].get_text(strip=True)

    url_cells = response.find_all('tr', class_='txtwhite12')
    audio_url = url_cells[0].find('a')['href']

    tz = ZoneInfo('Asia/Hong_Kong')
    today = dt.datetime.now(tz)
    year = today.year
    month = today.month
    day = today.day

    date_string = f"{year}年{month}月{day}日"

    message = f"""{date_string} [一日一恩典]
《天天天言》- {title_zh}
閲讀原文：
{url}
收聽：
{audio_url}
"""

    response = send_pushover_message(message)
    print(f"Pushover Response Status: {response.get('status')}")


if __name__ == '__main__':
    main()
