import calendar
import pandas as pd
import streamlit as st
from dataclasses import dataclass
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from utils.flow.utils.utils import get_week_range


@dataclass
class OMIncome:
    om_df: pd.DataFrame

    def get(self, day, return_dict=True):
        income = {}
        for _, row in self.om_df.iterrows():
            payment_day = self.get_payment_data(
                day, row["Dia da emissão"], row["Prazo pagamento"]
            )
            if payment_day:
                income[row["OM"]] = (payment_day, row["Valor"])
        if return_dict:
            return income
        else:
            return self.format_return(income)

    def get_payment_data(self, day, base_day, delay_time):
        first_day_of_week, last_day_of_week = get_week_range(day)
        max_previous_months = delay_time // 28 + 1

        for prev_month_count in range(0, max_previous_months + 1):
            try:
                prev_month = (
                    date(day.year, day.month, base_day)
                    - relativedelta(months=prev_month_count)
                    + timedelta(days=delay_time)
                )
            except ValueError:
                prev_month = (
                    date(
                        day.year, day.month, calendar.monthrange(day.year, day.month)[1]
                    )
                    - relativedelta(months=prev_month_count)
                    + timedelta(days=delay_time)
                )
            if first_day_of_week <= prev_month <= last_day_of_week:
                return prev_month

    def format_return(self, income_dict):
        totals = []
        for om, details in income_dict.items():
            totals.append(
                {"name": om, "date": details[0], "value": details[1], "is_income": 1}
            )
        return pd.DataFrame(totals)
