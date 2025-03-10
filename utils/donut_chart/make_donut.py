from multiprocessing.spawn import prepare

import pandas as pd
import altair as alt
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


def make_donut(om, column, df, actual_expenses):
    df = treat_df_to_bar_chart(om, df, actual_expenses)
    df = df[df["expenses"] == column]

    predict = df[df["type"] == "predict"]["value"].tolist()[0]
    actual = df[df["type"] == "actual"]["value"].tolist()[0]
    diff = predict - actual

    color = "green" if diff > 0 else "red"
    if predict == 0:
        predict = 0.00000001
    value = int(actual / predict * 100) if diff > 0 else int(diff / predict * 100)
    return make_donut_chart(value, om, color)
    # color = "green" if diff > 0 else "red"
    # value =

    st.write(df)


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


def make_donut_chart(input_response, input_text, input_color):
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
        baseline="middle",  # Garante que o texto fique centralizado verticalmente
        dx=0,  # Deslocamento horizontal
        dy=0,  # Deslocamento vertical
        color="black",  # Cor neutra pra testar
        font="Arial",  # Fonte padrão
        fontSize=32,
        fontWeight=700,
        fontStyle="italic",
    ).encode(
        # Em vez de text=alt.value(...), você pode usar:
        text=alt.value(f"{input_response} %")
    )

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
