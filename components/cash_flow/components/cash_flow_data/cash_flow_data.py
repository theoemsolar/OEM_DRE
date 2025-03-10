import calendar
from calendar import month

import pandas as pd
import streamlit as st
from datetime import date, timedelta
from dataclasses import dataclass, field

from utils import OMIncome, OMExpense

import plotly.graph_objects as go


MONTHS = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


@dataclass
class CashFlowData:
    om_data: pd.DataFrame
    expenses_data: pd.DataFrame
    dashboard_df: pd.DataFrame

    title: str = field(init=False)
    today: date = field(init=False)
    income: OMIncome = field(init=False)
    last_day_of_week: date = field(init=False)
    first_day_of_week: date = field(init=False)

    def __post_init__(self):
        self.today = date.today()

        self.outcome = OMExpense(self.om_data, self.dashboard_df, self.expenses_data)
        self.income = OMIncome(self.om_data)

    def get_weeks_of_month(self, year: int, month: int):
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)
        next_month_day = 1
        new_weeks = []
        for week in month_days:
            if not week[0] == 0:
                for day in week:
                    if day == 0:
                        if month == 12:
                            week[week.index(day)] = date(year, 1, next_month_day)
                        else:
                            week[week.index(day)] = date(
                                year, month + 1, next_month_day
                            )
                        next_month_day += 1
                    else:
                        week[week.index(day)] = date(year, month, day)
                new_weeks.append(week)
        return new_weeks

    def get_week_summary_title(self):
        weeks = self.get_weeks_of_month(
            st.session_state.current_week.year, st.session_state.current_week.month
        )

        if st.session_state.current_week not in [
            week_day for week in weeks for week_day in week
        ]:
            weeks = (
                self.get_weeks_of_month(
                    st.session_state.current_week.year,
                    st.session_state.current_week.month - 1,
                )
                if st.session_state.current_week.month != 1
                else self.get_weeks_of_month(
                    st.session_state.current_week.year,
                    12,
                )
            )

        diff = int((st.session_state.current_week - self.today).days / 7)
        diff_label = f"+ {diff}" if diff > 0 else f"{diff}"

        current_week = st.session_state.current_week

        for index, week in enumerate(weeks, start=1):
            if current_week in week:
                month_name = MONTHS[week[0].month - 1]
                self.title = f"{index} semana de {month_name} :grey[({diff_label})]"
                return

        month_name = MONTHS[current_week.month - 1]
        self.title = f"5 semana de {month_name} :grey[({diff_label})]"
