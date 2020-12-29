from datetime import date


def get_date_by_russian_date(day_text: str, year: int) -> date:
    day, month = day_text.split()
    month = translate_month_name(month)
    day = int(day)
    return date(year, month, day)


def translate_month_name(month_name_ru: str) -> int:
    converter = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
    }
    try:
        return converter[month_name_ru]
    except KeyError:
        raise ValueError(
            "In month mast be str with russian name of month, "
            f"found {month_name_ru}"
        )
