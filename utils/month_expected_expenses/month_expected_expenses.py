import calendar
from collections import defaultdict
from utils import OMExpense


def get_month_expected_expenses(day, contract_info_df, expenses_df, dates_df):
    totals = defaultdict(int)
    for week in months_day(day.year, day.month):
        for day in week:
            day_expenses = OMExpense(contract_info_df, expenses_df, dates_df).by_day(
                day
            )
            for expense, value in day_expenses.items():
                totals[expense] += value
    return totals


def months_day(ano, mes):
    week = calendar.Calendar(6).monthdatescalendar(ano, mes)
    return week[1:] if week[0][0].month != mes else week
