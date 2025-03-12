import datetime
from collections import defaultdict
from dataclasses import dataclass, field

import pandas as pd
import sys
import os

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.flow.utils.utils import get_week_range
from utils.flow.expenses.expenses_by_fixed_date import ExpenseByFixedDate
from utils.flow.expenses.expenses_by_business_day import ExpensesByBusinessDay
from utils.flow.expenses.expenses_by_issue_note import ExpenseByIssueNote


@dataclass
class OMExpense:
    contract_info_df: pd.DataFrame
    expenses_df: pd.DataFrame
    dates_df: pd.DataFrame
    expenses_by_business_day: ExpensesByBusinessDay = field(init=False)
    expenses_by_fixed_date: ExpenseByFixedDate = field(init=False)
    expenses_by_issue_note: ExpenseByIssueNote = field(init=False)

    def __post_init__(self):
        self.expenses_by_business_day = ExpensesByBusinessDay(
            self.contract_info_df, self.expenses_df, self.dates_df
        )
        self.expenses_by_fixed_date = ExpenseByFixedDate(
            self.contract_info_df, self.expenses_df, self.dates_df
        )
        self.expenses_by_issue_note = ExpenseByIssueNote(
            self.contract_info_df, self.expenses_df, self.dates_df
        )

    def by_day(self, day):
        return (
            self.expenses_by_business_day.get_expenses_business_day(day)
            | self.expenses_by_fixed_date.get_expenses_fix_date(day)
            | self.expenses_by_issue_note.get_expenses_issue_note(day)
        )

    def by_week(self, date, return_dict=True):
        totals = defaultdict(list)
        first_day_of_week, last_day_of_week = get_week_range(date)
        for delta in range((last_day_of_week - first_day_of_week).days + 1):
            current_date = first_day_of_week + datetime.timedelta(delta)
            for expense, value in self.by_day(current_date).items():
                totals[expense].append({"date": current_date, "value": value})

        if return_dict:
            return totals
        return self.format_return(totals)

    def format_return(self, income_dict):
        totals = []
        for om, details in income_dict.items():
            for expense in details:
                totals.append(
                    {
                        "name": om,
                        "date": expense["date"],
                        "value": expense["value"],
                        "is_income": 0,
                    }
                )
        return pd.DataFrame(totals)
