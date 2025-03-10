import math
import pandas as pd
import streamlit as st

from datetime import date
from reportlab.lib.colors import black, white, HexColor, red, green
from reportlab.lib.units import cm

from utils import get_month_expected_expenses
from mensal_summary.month_metrics.month_metrics import (
    month_metrics,
    mock_actual_expenses,
    format_currency,
)


def activity_table(c, dashboard_df, om_data, expenses_data, font_size=12):
    df = build_df(dashboard_df, om_data, expenses_data)
    table_data = create_table_data_from_df(df)
    x = 2 * cm
    y = 20 * cm
    draw_table(c, table_data, x, y, font_size)


def build_df(dashboard_df, om_data, expenses_data):
    month_expected_expenses = get_month_expected_expenses(
        date.today(), dashboard_df, om_data, expenses_data
    )

    data = [
        {
            "activity": activity,
            "predict": predict,
            "actual": mock_actual_expenses.get(activity, 0),
            "diff": predict - mock_actual_expenses.get(activity, 0),
        }
        for activity, predict in month_expected_expenses.items()
    ]

    return pd.DataFrame(data)


def create_table_data_from_df(df: pd.DataFrame):

    table_data = [["Atividade", "Previsto", "Realizado", "Diferença"]]
    for _, row in df.iterrows():
        previsto = format_currency(row["predict"])
        realizado = format_currency(row["actual"])
        diff = row["diff"]
        if diff == 0:
            diff_str = f"— {format_currency(diff)}"
        else:
            arrow = "▲" if diff >= 0 else "▼"
            diff_str = f"{arrow} {format_currency(abs(diff))}"
        table_data.append([row["activity"], previsto, realizado, diff_str])
    return table_data


def draw_table(c, data, x, y, font_size=10):

    padding = 8
    row_height = max(1 * cm, font_size + padding)
    total_width = sum([5 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm])
    current_y = y

    vertical_offset = (row_height - font_size) / 2

    for row_idx, row in enumerate(data):
        is_header = row_idx == 0
        c.setFillColor(HexColor("#004F8B")) if is_header else c.setFillColor(white)
        c.rect(x, current_y - row_height, total_width, row_height, fill=1, stroke=0)
        cell_x = x
        for col_idx, cell_text in enumerate(row):

            font = (
                set_header(c)
                if is_header
                else set_none_header(c, cell_text, col_idx, font)
            )
            c.setFont(font, font_size)
            offset_x = 5
            c.drawString(
                cell_x + offset_x,
                current_y - row_height + vertical_offset,
                str(cell_text),
            )
            c.setStrokeColor(black)
            c.line(cell_x, current_y - row_height, cell_x, current_y)
            cell_x += [5 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm][col_idx]
        c.line(x + total_width, current_y - row_height, x + total_width, current_y)
        c.line(x, current_y - row_height, x + total_width, current_y - row_height)
        current_y -= row_height
    c.line(x, y, x + total_width, y)


def set_none_header(c, cell_text, col_idx, font):
    if col_idx == 3:
        if str(cell_text).strip().startswith("▲"):
            c.setFillColor(green)
        elif str(cell_text).strip().startswith("▼"):
            c.setFillColor(red)
        else:
            c.setFillColor(black)
    else:
        c.setFillColor(black)
    font = "Helvetica"
    return font


def set_header(c):
    c.setFillColor(white)
    font = "Helvetica-Bold"
    return font
