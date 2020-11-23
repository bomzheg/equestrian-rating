from openpyxl import load_workbook
from openpyxl.worksheet import worksheet


MAX_ROW_SEARCH = 1000
DAY_ROW = 1
YEAR_ROW = 2
HORSE_NAME_ROW = 3
ATHLETE_NAME_ROW = 4
CLUB_NAME_ROW = 5


def parse_workbook(file):
    wb = load_workbook(file)
    for ws in wb.worksheets:
        parse_worksheet(ws)


def parse_worksheet(ws: worksheet):
    row = search_first_line(ws)
    while not is_empty_row(ws, row):
        day = ws.cell(row=row, col=DAY_ROW).value
        year = ws.cell(row=row, col=YEAR_ROW).value
        horse_name = ws.cell(row=row, col=HORSE_NAME_ROW).value
        athlete_name = ws.cell(row=row, col=ATHLETE_NAME_ROW).value
        club_name = ws.cell(row=row, col=CLUB_NAME_ROW).value



def search_first_line(ws: worksheet):
    for row_index in range(1, MAX_ROW_SEARCH):
        if ws.cell(row=row_index, col=DAY_ROW).value == "Дата":
            return row_index + 1  # use next row after header


def is_empty_row(ws: worksheet, row: int):
    return ws.cell(row=row, col=DAY_ROW).value is None


def save_results(results, to_standard):
    pass
