import pandas as pd
from datetime import timedelta
from collections import defaultdict
from dataclasses import dataclass, field

COLUMNS = ["Imposto"]


@dataclass
class ExpenseByIssueNote:
    dates_df: pd.DataFrame
    expenses_df: pd.DataFrame
    contract_info_df: pd.DataFrame
    merged_df: pd.DataFrame = field(init=False)

    def get_expenses_issue_note(self, date):
        self.merged_df = pd.merge(self.dates_df, self.expenses_df, on="OM")
        return self.calculate_expenses(date)

    def calculate_expenses(self, date):
        totals = defaultdict(int)
        for _, row in self.merged_df.iterrows():
            for column in COLUMNS:
                payment_day = date - timedelta(
                    self.contract_info_df[f"data da {column}"].tolist()[0],
                )
                if payment_day.day == row["Dia da emissão"]:
                    totals[column] += row[column]
        return totals
