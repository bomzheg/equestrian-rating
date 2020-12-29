import os
from pathlib import Path

import requests
import bs4
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv(BASE_DIR / ".env")

EQUESTRIAN_LOGIN = os.getenv('EQUESTRIAN_LOGIN')
EQUESTRIAN_PASSWORD = os.getenv('EQUESTRIAN_PASSWORD')
URL = "https://www.equestrian.ru/sport/jw_stat/?date_start=2019-10-01&date_end=2019-10-31&height_min=80&height_max=80"
LOGIN_URL = "https://www.equestrian.ru/login.php"


def authorize(login_url: str, login: str, password: str) -> dict:
    response = requests.post(
        login_url,
        headers={"ContentType": "application/x-www-form-urlencoded"},
        data={"login": login, "passwd": password, "returnto": "/"}
    )
    if not response.ok:
        raise IOError
    return {"Cookie": response.request.headers['Cookie']}


def download_page(cookies: dict, url: str) -> str:
    response = requests.get(url, cookies=cookies)
    if not response.ok:
        raise IOError
    return response.text


def get_url() -> str:
    return URL


def parse(html_text: str):
    pass


def save_page():
    cookie = authorize(LOGIN_URL, EQUESTRIAN_LOGIN, EQUESTRIAN_PASSWORD)
    page = download_page(cookie, get_url())
    with open("page.html", "w") as f:
        f.write(page)


def load_page():
    with open("page.html", "r") as f:
        html_page = f.read()
    return html_page


if __name__ == '__main__':
    parse(load_page())
