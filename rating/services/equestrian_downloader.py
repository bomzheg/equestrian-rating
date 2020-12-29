import typing
from datetime import date

import requests
_URL_STAT_TEMPLATE = "https://www.equestrian.ru/sport/"


class EquestrianDownloader:
    LOGIN_URL = "https://www.equestrian.ru/login.php"

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.cookie: dict = {}

    def create_session(self):
        self.cookie = self._authorize()

    def download_jumping(self, date_from: date, date_to: date, height_from: int, height_to: int):
        return self._download_page(*_get_url_jumping(date_from, date_to, height_from, height_to))

    def download_dressage(self, date_from: date, date_to: date, percent_from: int, percent_to: int = 100):
        return self._download_page(*_get_url_dressage(date_from, date_to, percent_from, percent_to))

    def _download_page(self, url: str, payload: dict) -> str:
        if len(self.cookie) == 0:
            self.create_session()
        response = requests.get(url, cookies=self.cookie, params=payload)
        if not response.ok:
            raise IOError
        return response.text

    def _authorize(self):
        response = requests.post(
            self.LOGIN_URL,
            headers={"ContentType": "application/x-www-form-urlencoded"},
            data={"login": self.login, "passwd": self.password, "returnto": "/"}
        )
        if not response.ok:
            raise IOError
        return {"Cookie": response.request.headers['Cookie']}


def _get_url_jumping(date_from: date, date_to: date, height_from: int, height_to: int) -> typing.Tuple[str, dict]:
    """
    this function return payload and url
    url like https://www.equestrian.ru/sport/jw_stat/
    payload like date_start=2019-10-01&date_end=2019-10-31&height_min=80&height_max=80
    """
    url_template = _URL_STAT_TEMPLATE + "jw_stat"
    payload = _get_date_payload(date_from, date_to)
    height_from_key = "height_min"
    height_to_key = "height_max"
    payload.update({
        height_from_key: height_from,
        height_to_key: height_to,
    })
    return url_template, payload


def _get_url_dressage(date_from: date, date_to: date, percent_from: int, percent_to: int) -> typing.Tuple[str, dict]:
    """
    this function return payload and url
    url like https://www.equestrian.ru/sport/dr_stat/
    payload like date_start=2020-01-01&date_end=2020-12-29&test=&proc_min=66&proc_max=100
    """
    url_template = _URL_STAT_TEMPLATE + "dr_stat"
    payload = _get_date_payload(date_from, date_to)
    percent_from_key = "proc_min"
    percent_to_key = "proc_max"
    payload.update({
        percent_from_key: percent_from,
        percent_to_key: percent_to,
    })
    return url_template, payload


def _get_date_payload(date_from: date, date_to: date) -> dict:
    date_from_key = "date_start"
    date_to_key = "date_end"
    payload = {
        date_from_key: date_from,
        date_to_key: date_to,
    }
    return payload
