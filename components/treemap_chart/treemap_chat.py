import base64
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass
import math
import numpy as np
import altair as alt
from streamlit_plotly_events import plotly_events
from components.treemap_chart.mock_api import actual_expenses

COLUMNS_TO_SHOW = [
    "Roçagem e Limpeza Mensal",
    "Custo OP",
    "Comissão",
    "Folha ADM",
    "Imposto",
    "Bancagem",
    "Custo Fixo",
]


def distribuir_elementos(lista, max_colunas=5):
    n = len(lista)
    colunas = min(max_colunas, math.ceil(math.sqrt(n)))
    linhas = math.ceil(n / colunas)
    tabela = [[] for _ in range(colunas)]
    for i, elemento in enumerate(lista):
        tabela[i % colunas].append(elemento)
    return tabela


def make_donut(input_response, input_text, input_color):
    chart_colors = {
        "blue": ["#29b5e8", "#155F7A"],
        "green": ["#27AE60", "#12783D"],
        "orange": ["#F39C12", "#875A12"],
        "red": ["#E74C3C", "#781F16"],
    }
    chart_color = chart_colors.get(input_color, ["#29b5e8", "#155F7A"])

    source = pd.DataFrame(
        {"Topic": ["", input_text], "% value": [100 - input_response, input_response]}
    )
    source_bg = pd.DataFrame({"Topic": ["", input_text], "% value": [100, 0]})

    plot = (
        alt.Chart(source)
        .mark_arc(innerRadius=45, cornerRadius=25)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(domain=[input_text, ""], range=chart_color),
                legend=None,
            ),
        )
        .properties(width=130, height=130)
    )

    text = plot.mark_text(
        align="center",
        color="#29b5e8",
        font="Lato",
        fontSize=32,
        fontWeight=700,
        fontStyle="italic",
    ).encode(text=alt.value(f"{input_response} %"))

    plot_bg = (
        alt.Chart(source_bg)
        .mark_arc(innerRadius=45, cornerRadius=20)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(domain=[input_text, ""], range=chart_color),
                legend=None,
            ),
        )
        .properties(width=130, height=130)
    )
    return plot_bg + plot + text


@dataclass
class TreemapChart:
    dashboard_df: pd.DataFrame

    def show(self):
        if st.session_state.om_selected:
            col1, col2, col3 = st.columns([15, 15, 70], gap="large")
            with col1:
                if st.button("Voltar", use_container_width=True):
                    st.session_state.update(om_selected=None)
                    st.rerun()
            with col3:
                st.title(st.session_state.om_selected)
            self.show_data_graph()
        else:
            self.select_om()

    def select_om(self):
        table = distribuir_elementos(self.dashboard_df["OM"], max_colunas=5)
        cols = st.columns(len(table), gap="small")

        for col, oms in zip(cols, table):
            with col:
                for om in oms:
                    if st.button(om, use_container_width=True):
                        st.session_state.om_selected = om
                        st.rerun()

    def show_data_graph(self):
        df = self.treat_df_to_bar_chart()
        self.donut_charts(df)
        self.show_bar_cahrt(df)

    def show_bar_cahrt(self, df):
        fig = go.Figure()
        df_pivot = df.pivot(index="expenses", columns="type", values="value")

        fig.add_trace(
            go.Bar(
                x=df_pivot.index,
                y=df_pivot["predict"],
                name="Previsto",
                marker_color="lightgreen",
                opacity=0.7,
            )
        )

        fig.add_trace(
            go.Bar(
                x=df_pivot.index,
                y=df_pivot["actual"],
                name="Real",
                marker_color="red",
                opacity=0.7,
            )
        )

        # Layout do gráfico
        fig.update_layout(
            xaxis_title="Despesas",
            yaxis_title="Valor (R$)",
            barmode="overlay",
            xaxis_tickangle=-45,
            legend=dict(x=0.8, y=1.0),
        )
        st.plotly_chart(fig)

    def donut_charts(self, df):
        table = distribuir_elementos(df["expenses"].unique())
        cols = st.columns(len(table), gap="small")

        for col, expenses in zip(cols, table):
            with col:
                for expense in expenses:
                    st.subheader(expense)
                    expense_df = df[df["expenses"] == expense]
                    predict = expense_df[expense_df["type"] == "predict"][
                        "value"
                    ].tolist()[0]
                    actual = expense_df[expense_df["type"] == "actual"][
                        "value"
                    ].tolist()[0]
                    diff = predict - actual

                    value = (
                        int(actual / predict * 100)
                        if diff > 0
                        else int(diff / predict * 100)
                    )
                    st.caption(f"Previsto: R${round(predict, 2)}")
                    st.caption(f"Gasto: R${round(actual, 2)}")
                    color = "green" if diff > 0 else "red"
                    donut_chart = make_donut(value, expense, color)
                    st.altair_chart(donut_chart, use_container_width=True)

    def treat_df_to_bar_chart(self):
        df = self.dashboard_df[self.dashboard_df["OM"] == st.session_state.om_selected]
        new_df_lines = []

        for column in df.columns:
            if column in COLUMNS_TO_SHOW:
                new_df_lines.append(
                    {
                        "expenses": column,
                        "type": "predict",
                        "value": df[column].tolist()[0],
                    }
                )
                new_df_lines.append(
                    {
                        "expenses": column,
                        "type": "actual",
                        "value": actual_expenses.get(
                            st.session_state.om_selected, {}
                        ).get(column, 0),
                    }
                )

        return pd.DataFrame(new_df_lines)
