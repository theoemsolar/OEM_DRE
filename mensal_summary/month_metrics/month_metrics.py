import math
import streamlit as st

from datetime import date
from reportlab.lib.pagesizes import A4

from utils import get_month_expected_expenses

mock_actual_expenses = {
    "Imposto": 90463.61,
    "Custo OP": 458364.17,
    "Comissão": 26197.81,
    "Folha ADM": 150937.99,
    "Bancagem": 72948.98,
    "Custo Fixo": 30000.00,
}


def month_metrics(c, dashboard_df, om_data, expenses_data):
    month_expected_expenses = get_total_month_expected_expenses(
        dashboard_df, om_data, expenses_data
    )
    month_actual_expenses = sum(mock_actual_expenses.values())
    add_diff(c, month_expected_expenses, month_actual_expenses)
    add_absolute_values(c, month_expected_expenses, month_actual_expenses)


def get_total_month_expected_expenses(dashboard_df, om_data, expenses_data):
    month_expected_expenses = get_month_expected_expenses(
        date.today(), dashboard_df, om_data, expenses_data
    )
    return sum(month_expected_expenses.values())


def add_diff(c, month_expected_expenses, month_actual_expenses):
    diff = month_expected_expenses - month_actual_expenses
    page_width, page_height = A4
    text_x = page_width / 2
    text_y = page_height - 170
    c.setFillColorRGB(0, 1, 0)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(text_x, text_y, format_currency(diff))
    draw_triangle(c, text_x - 115, text_y + 8, 30)


def add_absolute_values(c, month_expected_expenses, month_actual_expenses):
    page_width, page_height = A4
    text_y = page_height - 250
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(140, text_y, format_currency(month_expected_expenses))
    c.drawCentredString(440, text_y, format_currency(month_actual_expenses))

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(140, text_y + 30, "PREVISTO")
    c.drawCentredString(440, text_y + 30, "REALIZADO")


def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def draw_triangle(c, x, y, side, fill=1, stroke=0):
    R = side / math.sqrt(3)

    angles = [90, 210, 330]
    vertices = []
    for angle in angles:
        rad = math.radians(angle)
        vx = x + R * math.cos(rad)
        vy = y + R * math.sin(rad)
        vertices.append((vx, vy))

    p = c.beginPath()
    p.moveTo(vertices[0][0], vertices[0][1])
    for vx, vy in vertices[1:]:
        p.lineTo(vx, vy)
    p.close()

    c.drawPath(p, fill=fill, stroke=stroke)
