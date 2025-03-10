import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from datetime import timedelta
from dataclasses import dataclass

from streamlit import session_state

from components.cash_flow.components import CashFlowData
from components.cash_flow.utils import (
    get_week_range,
    format_float_to_cash,
)
from utils import OMExpense, OMIncome


@dataclass
class CashFlowDashboard(CashFlowData):
    om_data: pd.DataFrame
    expenses_data: pd.DataFrame
    dashboard_df: pd.DataFrame

    def show(self):
        self.navigation_commands()
        self.get_week_summary_title()
        self.show_individual_week_resume()

    def update_current_week(self):
        st.session_state.current_week = st.session_state.current_week_input

    def navigation_commands(self):
        if "current_week" not in st.session_state:
            st.session_state.current_week = self.today

        col1, col2, col3, col4 = st.columns([70, 4, 6, 4])

        with col2:
            if st.button("<-"):
                st.session_state.current_week -= timedelta(days=7)
                st.rerun()

        with col3:
            if st.button("Hoje"):
                st.session_state.current_week = self.today
                st.rerun()

        with col4:
            if st.button("->"):
                st.session_state.current_week += timedelta(days=7)
                st.rerun()

        col1, col2 = st.columns([86, 14])
        with col2:
            d = st.date_input(
                "",
                value=st.session_state.current_week,
                key="current_week_input",
                on_change=self.update_current_week,
            )

    def show_individual_week_resume(self):
        self.header()
        self.income = OMIncome(self.om_data).get(
            st.session_state.current_week, return_dict=False
        )
        self.expense = OMExpense(
            self.om_data, self.dashboard_df, self.expenses_data
        ).by_week(st.session_state.current_week, return_dict=False)
        general = pd.concat([self.income, self.expense])
        self.metrics(general)
        self.daily_flow_chart(general)
        self.list_of_movements(general)

    def header(self):
        first_day_of_week, last_day_of_week = get_week_range(
            st.session_state.current_week
        )
        st.title(self.title)
        st.caption(
            f"{first_day_of_week.strftime('%d/%m/%Y')} - {last_day_of_week.strftime('%d/%m/%Y')}"
        )

    def list_of_movements(self, general):
        general.sort_values("date", ascending=True, inplace=True)
        col1, col2 = st.columns(2)
        for row in general.itertuples():
            with col1:
                if row[4]:
                    st.write(
                        f"{row[2]} - {row[1]}: :green[{format_float_to_cash(row[3])}]"
                    )
            with col2:
                if not row[4]:
                    st.write(
                        f"{row[2]} - {row[1]}: :red[{format_float_to_cash(row[3])}]"
                    )

    def metrics(self, general):
        col1, col2, col3 = st.columns(3)
        with col1:
            # st.write(0 if len(self.expense) == 0 else self.income["value"].sum())
            st.metric(
                "GANHOS",
                f'{format_float_to_cash(0 if len(self.income) == 0 else self.income["value"].sum())}',
            )
        with col2:
            st.metric(
                "GASTOS",
                f'  {format_float_to_cash(0 if len(self.expense) == 0 else self.expense["value"].sum())}',
            )
        with col3:
            st.metric(
                "Caixa da semana",
                format_float_to_cash(
                    self.get_total_cash_by_week(st.session_state.current_week)
                ),
            )

    def get_total_cash_by_week(self, day):
        weeks = self.get_weeks_of_month(day.year, day.month)

        if day not in [week_day for week in weeks for week_day in week]:
            if day.month == 1:
                weeks = self.get_weeks_of_month(day.year - 1, day.month)
            else:
                weeks = self.get_weeks_of_month(day.year, day.month - 1)

        total_amount = 0

        for week in weeks:
            outcome = OMExpense(
                self.om_data, self.dashboard_df, self.expenses_data
            ).by_week(week[0], return_dict=False)
            income = OMIncome(self.om_data).get(week[0], return_dict=False)
            total_amount += 0 if len(income) == 0 else income["value"].sum()
            total_amount -= 0 if len(outcome) == 0 else outcome["value"].sum()

            if week[0] <= day <= week[-1]:
                return total_amount

    def daily_flow_chart(self, df):
        df["date"] = pd.to_datetime(df["date"])
        first_day_of_week, last_day_of_week = get_week_range(df["date"].min())
        full_date_range = pd.date_range(start=first_day_of_week, end=last_day_of_week)

        # Se a coluna is_income estiver em formato booleano, converta para inteiro (0 ou 1)
        if df["is_income"].dtype == bool:
            df["is_income"] = df["is_income"].astype(int)

        # Agrupamento por data e is_income
        grouped = df.groupby(["date", "is_income"])["value"].sum().unstack(fill_value=0)

        # Garante que ambas as categorias (0 e 1) existam no DataFrame
        grouped = grouped.reindex(columns=[0, 1], fill_value=0)

        # Reindexa as datas para o intervalo completo da semana
        grouped = grouped.reindex(full_date_range, fill_value=0)

        # Cria o gráfico
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=grouped.index.astype(str),
                y=grouped[0],
                name="Gastos",
                marker_color="red",
            )
        )
        fig.add_trace(
            go.Bar(
                x=grouped.index.astype(str),
                y=grouped[1],
                name="Ganhos",
                marker_color="green",
            )
        )
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Valor",
            barmode="group",
            xaxis=dict(type="category"),
        )
        st.plotly_chart(fig, use_container_width=True)
