import os
import typing
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
from time import sleep

from bs4 import BeautifulSoup
from bs4.element import Tag
from dotenv import load_dotenv

from rating.services.date_utils import get_date_by_russian_date
from rating.services.equestrian_downloader import EquestrianDownloader

BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv(BASE_DIR / ".env")

EQUESTRIAN_LOGIN = os.getenv('EQUESTRIAN_LOGIN')
EQUESTRIAN_PASSWORD = os.getenv('EQUESTRIAN_PASSWORD')
CAPTION_PATTERN = re.compile(r"Статистика по стартам \d{1,2}(?: [а-я]+)? — \d{1,2} [а-я]+ (\d{4})")


@dataclass
class ResultsParsing:
    date_: date
    horse_name: str = None
    athlete_name: str = None
    club: str = None


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
    except AttributeError:
        raise ValueError("Header parsing error. Perhaps you choose more that one year")


def parse_tr(tr: Tag, year: int) -> ResultsParsing:
    tds = tr.find_all("td")

    return ResultsParsing(
        date_=get_date_by_russian_date(tds[0].text, year),
        horse_name=tds[3].text,
        athlete_name=tds[4].text.title(),
        club=tds[6].text,
    )


def _save_page():
    downloader = EquestrianDownloader(EQUESTRIAN_LOGIN, EQUESTRIAN_PASSWORD)
    page = downloader.download_jumping(
        date(2020, 2, 1),
        date(2020, 10, 31),
        80,
        80,
    )
    with open("jumping.html", "w") as f:
        f.write(page)
    sleep(5)
    page = downloader.download_dressage(
        date(2020, 2, 1),
        date(2020, 10, 31),
        66,
    )
    with open("dressage.html", "w") as f:
        f.write(page)


def _load_page():
    with open("jumping.html", "r", encoding='1251') as f:
        html_page = f.read()
    return html_page


def write_csv(data: typing.List[ResultsParsing]):
    with open("results.csv", "w", encoding='utf-8') as f:
        f.write(f"Дата,Спортсмен,Лошадь,Клуб\n")
        for result in data:
            f.write(f"{result.date_.isoformat()},{result.athlete_name},{result.horse_name},{result.club}\n")


if __name__ == '__main__':
    _save_page()
    write_csv(parse(_load_page()))
