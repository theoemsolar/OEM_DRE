import calendar
import datetime
from datetime import date, timedelta


def get_week_range(day):
    weekday = day.weekday()
    sunday = day - timedelta(days=(weekday + 1) % 7)
    saturday = sunday + timedelta(days=6)
    return sunday, saturday


def get_equivalent_day(year, month, day):
    try:
        return datetime.date(year, month, day)
    except ValueError:
        last_day_of_month = calendar.monthrange(year, month)[1]
        diff = day - last_day_of_month
        return date(year, month, last_day_of_month) + timedelta(days=diff)


def add_business_days(start_date, business_days):
    weeks, extra_days = divmod(business_days, 5)
    new_date = start_date + timedelta(weeks=weeks)
    weekday = new_date.weekday()

    if weekday + extra_days < 5:
        new_date += timedelta(days=extra_days)
    else:
        new_date += timedelta(days=extra_days + 2)

    return new_date


def format_float_to_cash(value):
    return (
        f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if value
        else "R$ 00.00"
    )
