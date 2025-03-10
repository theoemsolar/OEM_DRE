from datetime import timedelta


def sub_business_days(start_date, business_days):
    current_date = start_date
    while business_days > 0:
        current_date -= timedelta(days=1)
        if current_date.weekday() < 5:
            business_days -= 1
    return current_date


def add_business_days(start_date, business_days):
    current_date = start_date
    while business_days > 0:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Segunda a sexta-feira (0 a 4)
            business_days -= 1
    return current_date


def get_equivalent_week_day(date):
    if date.weekday() == 5:
        return_date = date - timedelta(days=1)
    elif date.weekday() == 6:
        return_date = date - timedelta(days=2)
    else:
        return_date = date

    return return_date


def get_week_range(day):
    weekday = day.weekday()
    sunday = day - timedelta(days=(weekday + 1) % 7)
    saturday = sunday + timedelta(days=6)
    return sunday, saturday
