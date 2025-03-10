import pandas as pd
import streamlit as st

COLUMNS_TO_SHOW = [
    "Roçagem e Limpeza Mensal",
    "Custo OP",
    "Comissão",
    "Folha ADM",
    "Imposto",
    "Bancagem",
    "Custo Fixo",
]


def treat_df_to_bar_chart(om, dashboard_df, actual_expenses):
    df = dashboard_df[dashboard_df["OM"] == om]
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
                    "value": actual_expenses.get(om, {}).get(column, 0),
                }
            )

    return pd.DataFrame(new_df_lines)
