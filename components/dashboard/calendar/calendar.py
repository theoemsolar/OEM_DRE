from datetime import date, timedelta
import pandas as pd
import streamlit as st
from dataclasses import dataclass

from components.cash_flow.utils import get_week_range
from utils import OMIncome, OMExpense

# Remove o padding padrão das colunas do Streamlit
st.markdown(
    """
    <style>
        div[data-testid="column"] {
            padding: 0px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_week_range(today):
    start_of_week = today - timedelta(days=today.weekday())
    return [start_of_week + timedelta(days=i) for i in range(7)]


@dataclass
class Calendar:
    om_data: pd.DataFrame
    dashboard_df: pd.DataFrame
    expenses_data: pd.DataFrame

    def show(self):
        week_outcome = OMExpense(
            self.om_data, self.dashboard_df, self.expenses_data
        ).by_week(date.today())
        week_income = OMIncome(self.om_data).get(date.today())

        self.week_summary = week_outcome | week_income
        self.show_week()

    def show_week(self):
        week_days = get_week_range(date.today())
        self.css()
        html = self.week_calendar(week_days)
        st.markdown(html, unsafe_allow_html=True)

    def week_calendar(self, week_days):
        html = "<div class='calendar-grid'>"
        for day in week_days:
            html += "<div class='grid-item'>"
            # Exibe o dia abreviado e a data (ex.: Seg, 01/02)
            html += f"<div class='date'>{day.strftime('%a, %d/%m')}</div>"
            # Lista os eventos (income ou outcome) que ocorrem neste dia
            for name, infos in self.week_summary.items():
                if day == infos[0]:
                    html += f"<div class='event'>{name}</div>"
            html += "</div>"
        html += "</div>"
        return html

    def css(self):
        st.markdown(
            """
            <style>
                /* Fundo geral da página */
                body {
                    background-color: #121212;
                }
                /* Layout em grid para os dias da semana */
                .calendar-grid {
                    display: grid;
                    grid-template-columns: repeat(7, 1fr);
                    gap: 10px;
                    padding: 20px;
                }
                /* Cada item do grid (dia) */
                .grid-item {
                    background-color: #1e1e1e;
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid #333;
                    text-align: center;
                }
                /* Estilo da data */
                .date {
                    font-size: 1.1em;
                    font-weight: bold;
                    color: #ffffff;
                    margin-bottom: 8px;
                }
                /* Estilo dos eventos */
                .event {
                    font-size: 0.9em;
                    color: #cccccc;
                    margin-top: 4px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
