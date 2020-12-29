import os
import typing
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from dotenv import load_dotenv

from rating.services.date_utils import get_date_by_russian_date

BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv(BASE_DIR / ".env")

EQUESTRIAN_LOGIN = os.getenv('EQUESTRIAN_LOGIN')
EQUESTRIAN_PASSWORD = os.getenv('EQUESTRIAN_PASSWORD')
URL = "https://www.equestrian.ru/sport/jw_stat/?date_start=2019-10-01&date_end=2019-10-31&height_min=80&height_max=80"
LOGIN_URL = "https://www.equestrian.ru/login.php"
CAPTION_PATTERN = re.compile(r"Статистика по стартам \d{1,2} — \d{1,2} [а-я]+ (\d{4})")


@dataclass
class ResultsParsing:
    date_: date
    horse_name: str = None
    athlete_name: str = None
    club: str = None


def authorize(login_url: str, login: str, password: str) -> dict:
    response = requests.post(
        login_url,
        headers={"ContentType": "application/x-www-form-urlencoded"},
        data={"login": login, "passwd": password, "returnto": "/"}
    )
    if not response.ok:
        raise IOError
    return {"Cookie": response.request.headers['Cookie']}


def download_page(cookies: dict, url: str, payload: dict) -> str:
    response = requests.get(url, cookies=cookies, params=payload)
    if not response.ok:
        raise IOError
    return response.text


def get_url_jumping(date_from, date_to, height_from, height_to) -> typing.Tuple[str, dict]:
    """
    this function return payload and url
    payload like date_start=2019-10-01&date_end=2019-10-31&height_min=80&height_max=80
    """
    url_template = "https://www.equestrian.ru/sport/jw_stat"
    date_from_key = "date_start"
    date_to_key = "date_end"
    height_from_key = "height_min"
    height_to_key = "height_max"
    payload = {
        date_from_key: date_from,
        date_to_key: date_to,
        height_from_key: height_from,
        height_to_key: height_to,
    }
    return url_template, payload


def parse(html_text: str):
    """
    Данный метод парсит исключительно в пределах одного года!
    """
    soup = BeautifulSoup(html_text, "lxml")
    table = soup.find("table", class_="stat")
    header = soup.find("h2")
    year = get_year_from_header(header.text)
    check_table_head(table)
    results = []
    for tr in table.find_all("tr", attrs={'class': None}):
        results.append(parse_tr(tr, year))
    return results


def check_table_head(table: Tag):
    standard_head = [
        "Дата",
        "Маршрут",
        "Место",
        "Лошадь",
        "Спортсмен",
        "Разряд",
        "Клуб",
    ]
    try:
        head = table.find("tr", class_="head")
        ths = head.find_all("th")
        if not all([th.text == th_std for th, th_std in zip(ths, standard_head)]):
            raise AttributeError
    except AttributeError:
        raise ValueError("Table structure perhaps changed. Parsing can't be continued")


def get_year_from_header(header: str) -> int:
    try:
        year = CAPTION_PATTERN.match(header).group(1)
        return int(year)
    except (ValueError, TypeError, IndexError):
        raise ValueError("Header parsing error. Perhaps you choose more that one year")


def parse_tr(tr: Tag, year: int) -> ResultsParsing:
    tds = tr.find_all("td")

    return ResultsParsing(
        date_=get_date_by_russian_date(tds[0].text, year),
        horse_name=tds[3].text,
        athlete_name=tds[4].text.title(),
        club=tds[6].text,
    )


def save_page():
    cookie = authorize(LOGIN_URL, EQUESTRIAN_LOGIN, EQUESTRIAN_PASSWORD)
    page = download_page(cookie, *get_url_jumping(
        date(2020, 10, 1),
        date(2020, 10, 31),
        80,
        80,
    ))
    with open("page.html", "w") as f:
        f.write(page)


def load_page():
    with open("page.html", "r", encoding='1251') as f:
        html_page = f.read()
    return html_page


def write_csv(data: typing.List[ResultsParsing]):
    with open("results.csv", "w", encoding='utf-8') as f:
        f.write(f"Дата,Спортсмен,Лошадь,Клуб\n")
        for result in data:
            f.write(f"{result.date_.isoformat()},{result.athlete_name},{result.horse_name},{result.club}\n")


if __name__ == '__main__':
    save_page()
    write_csv(parse(load_page()))
