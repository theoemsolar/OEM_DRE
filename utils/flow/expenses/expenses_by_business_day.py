import pandas as pd
import streamlit as st
from dataclasses import dataclass, field
from datetime import date
from collections import defaultdict

from utils.flow.utils.utils import (
    get_equivalent_week_day,
    sub_business_days,
    add_business_days,
)

COLUMNS = ["Custo OP", "Comissão", "Folha ADM"]


@dataclass
class ExpensesByBusinessDay:
    dates_df: pd.DataFrame
    expenses_df: pd.DataFrame
    contract_info_df: pd.DataFrame
    merged_df: pd.DataFrame = field(init=False)

    def get_expenses_business_day(self, day):
        self.merged_df = pd.merge(self.dates_df, self.expenses_df, on="OM")
        return self.get_payment_dates(day)

    def get_payment_dates(self, day):
        totals = defaultdict(int)
        for _, row in self.merged_df.iterrows():
            self.check_individual_om(day, row, totals)

        return totals

    def check_individual_om(self, day, row, totals):
        for column in COLUMNS:
            payment_day = add_business_days(
                date(day.year, day.month, 1),
                self.contract_info_df[f"data da {column}"].tolist()[0],
            )
            if payment_day == day:
                totals[column] += row[column]
