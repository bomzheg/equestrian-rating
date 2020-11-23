import typing
from datetime import date

from django.db.models import Manager
from openpyxl import load_workbook
from openpyxl.worksheet import worksheet

from rating.models import Result, Standard

MAX_ROW_SEARCH = 1000
DAY_ROW = 1
YEAR_ROW = 2
HORSE_NAME_ROW = 3
ATHLETE_NAME_ROW = 4
CLUB_NAME_ROW = 5


def parse_workbook(file) -> typing.List[Result]:
    wb = load_workbook(file)
    results = []
    for ws in wb.worksheets:
        results.extend(parse_worksheet(ws))
    return results


def parse_worksheet(ws: worksheet) -> typing.List[Result]:
    row = search_first_line(ws)
    standard = get_standard(ws)
    results = []
    while not is_empty_row(ws, row):
        day = ws.cell(row=row, col=DAY_ROW).value
        year = ws.cell(row=row, col=YEAR_ROW).value
        horse_name = ws.cell(row=row, col=HORSE_NAME_ROW).value
        athlete_name = ws.cell(row=row, col=ATHLETE_NAME_ROW).value
        club_name = ws.cell(row=row, col=CLUB_NAME_ROW).value
        date_ = get_date_by_russian_date(day, year)
        results.append(Result(
            fulfilled_standard=standard,
            date=date_,
            horse_name=horse_name,
            athlete_name=athlete_name,
            club_name=club_name,
        ))
    return results


def get_standard(ws: worksheet) -> Standard:
    raise NotImplemented


def get_date_by_russian_date(day_text: str, year: int) -> date:
    raise NotImplemented


def search_first_line(ws: worksheet) -> int:
    for row_index in range(1, MAX_ROW_SEARCH):
        if ws.cell(row=row_index, col=DAY_ROW).value == "Дата":
            return row_index + 1  # use next row after header


def is_empty_row(ws: worksheet, row: int) -> bool:
    return ws.cell(row=row, col=DAY_ROW).value is None


def save_results(results: typing.List[Result], using=None):
    # noinspection PyUnresolvedReferences
    Result.objects.bulk_create(results, using=using)
