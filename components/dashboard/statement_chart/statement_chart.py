import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
from api.sheet_data import SheetData
from datetime import date, timedelta
from utils import OMExpense, OMIncome

if "time_period" not in st.session_state:
    st.session_state.time_period = "M"

if "graph_option" not in st.session_state:
    st.session_state.graph_option = "line"


@st.cache_data
def load_data():
    sheet_data = SheetData()
    dashboard_df = sheet_data.get_dashboard_data()
    dashboard_df.rename(columns={dashboard_df.columns[0]: "OM"}, inplace=True)
    om_data = sheet_data.get_OM_datas()
    expenses_data = sheet_data.get_expenses()
    return dashboard_df, om_data, expenses_data


def convert_currency(value):
    if isinstance(value, str):
        value = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(value) if value else 0.0
    return value


dashboard_df, om_data, expenses_data = load_data()

columns_to_convert = dashboard_df.columns[2:]
for col in columns_to_convert:
    if col != "Margem":
        dashboard_df[col] = dashboard_df[col].apply(convert_currency)

om_data["Valor"] = om_data["Valor"].apply(convert_currency)

day = date(2025, 5, 2)


@st.cache_data
def get_outcomes():
    outcomes = {}
    day_aux = date(2025, 1, 1)
    for _ in range(365):
        outcome = OMExpense(dashboard_df, om_data, expenses_data).by_day(day_aux)
        outcomes[day_aux.strftime("%d/%m/%y")] = dict(outcome)
        day_aux += timedelta(days=1)
    return pd.DataFrame(outcomes).T * -1


@st.cache_data
def get_incomes():
    om_dict = defaultdict(dict)
    day_aux = date(2025, 1, 1)
    for _ in range(365):
        income = OMIncome(om_data).get(day_aux)
        for om, data in income.items():
            om_dict[data[0].strftime("%d/%m/%y")][om] = data[1]
        day_aux += timedelta(days=1)
    return pd.DataFrame(om_dict).T


def get_accumulate(outcomes_df, incomes_df):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.graph_option = st.radio(
            "Gráfico", ["line", "vela", "ohlc"], horizontal=True
        )
    with col2:
        time = st.radio("Tempo", ["semanal", "mensal"], horizontal=True)
        st.session_state.time_period = "W" if time == "semanal" else "M"

    flow_df = outcomes_df.join(incomes_df).sum(axis=1)
    accumulate = flow_df.cumsum()
    accumulate = pd.DataFrame(accumulate).rename({0: "value"}, axis=1)
    accumulate.index = pd.to_datetime(accumulate.index)
    df_ohlc = accumulate["value"].resample(st.session_state.time_period).ohlc()

    if st.session_state.graph_option == "line":
        fig = px.line(df_ohlc["close"])
    elif st.session_state.graph_option == "vela":
        fig = plot_candlestick(df_ohlc)
    elif st.session_state.graph_option == "ohlc":
        fig = plot_ohlc(df_ohlc)

    st.plotly_chart(fig)


def plot_candlestick(df_ohlc):
    fig = go.Figure(
        data=go.Candlestick(
            x=df_ohlc.index,
            open=df_ohlc["open"],
            high=df_ohlc["high"],
            low=df_ohlc["low"],
            close=df_ohlc["close"],
            increasing_line_color="green",
            decreasing_line_color="red",
        )
    )
    fig.update_layout(
        title="Candlestick Mensal",
        xaxis_title="Data",
        yaxis_title="Valor",
        xaxis_rangeslider_visible=False,
    )
    return fig


def plot_ohlc(df_ohlc):
    fig = go.Figure(
        data=go.Ohlc(
            x=df_ohlc.index,
            open=df_ohlc["open"],
            high=df_ohlc["high"],
            low=df_ohlc["low"],
            close=df_ohlc["close"],
            increasing_line_color="green",
            decreasing_line_color="red",
        )
    )
    fig.update_layout(
        title="Gráfico OHLC Mensal",
        xaxis_title="Data",
        yaxis_title="Valor",
        xaxis_rangeslider_visible=False,
    )
    return fig


def statement_chart():
    outcomes_df = get_outcomes()
    incomes_df = get_incomes()
    get_accumulate(outcomes_df, incomes_df)
