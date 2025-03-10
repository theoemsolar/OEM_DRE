import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from dataclasses import dataclass
from components.treemap_chart.mock_api import actual_expenses


@dataclass
class Metrics:
    predict_df: pd.DataFrame

    def show(self):
        predict = self.predict_df["Total custo"].sum()
        actual = self.get_total_actual_expenses()
        # actual = 1000000
        bar_color = "green" if actual < predict else "red"

        fig = go.Figure(
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=actual,
                mode="gauge+number+delta",
                title={"text": "Fevereiro"},
                delta={
                    "reference": predict,
                    "increasing": {"color": "red"},
                    "decreasing": {"color": "green"},
                },
                gauge={"axis": {"range": [None, predict]}, "bar": {"color": bar_color}},
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    def get_total_actual_expenses(self):
        return sum(
            [expense for om in actual_expenses.values() for expense in om.values()]
        )
