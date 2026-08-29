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
    url = 'https://pushover.net'
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

    # Fetch and enforce proper traditional Chinese encoding
    res = requests.get(url)
    res.encoding = 'big5_hkscs'

    soup = BeautifulSoup(res.text, 'html.parser')

    # Fixed bug: Changed find_all to find so .get_text() works seamlessly
    title_element = soup.find('td', class_='devotiontxtbold2')
    url_element = soup.find('tr', class_='txtwhite12')

    # Defensive check if site format changes unexpectedly
    if not title_element or not url_element or not url_element.find('a'):
        raise RuntimeError(
            "Failed to parse website elements. The site layout might have updated.")

    title_zh = title_element.get_text(strip=True)
    audio_url = url_element.find('a')['href']

    # Get local Hong Kong Time date
    tz = ZoneInfo('Asia/Hong_Kong')
    today = dt.datetime.now(tz)
    date_string = f"{today.year}年{today.month}月{today.day}日"

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
