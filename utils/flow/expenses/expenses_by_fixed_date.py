from dataclasses import dataclass, field
import pandas as pd
import streamlit as st
from collections import defaultdict

COLUMNS = ["Bancagem", "Custo Fixo"]


@dataclass
class ExpenseByFixedDate:
    dates_df: pd.DataFrame
    expenses_df: pd.DataFrame
    contract_info_df: pd.DataFrame
    merged_df: pd.DataFrame = field(init=False)

    def get_expenses_fix_date(self, date):
        self.merged_df = pd.merge(self.dates_df, self.expenses_df, on="OM")
        return self.calculate_expenses(date)

    def calculate_expenses(self, date):
        totals = defaultdict(int)
        for _, row in self.merged_df.iterrows():
            for column in COLUMNS:
                if date.day == self.contract_info_df[f"data da {column}"].tolist()[0]:
                    totals[column] += row[column]

        return totals
