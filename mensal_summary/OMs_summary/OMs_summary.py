import os

from utils import make_donut
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


def oms_summary(c, dashboard_df, om_data, expenses_data):
    y = 700
    for om in dashboard_df["OM"]:
        add_OM_info(c, om, dashboard_df, y)
        y -= 140
        if y <= 10:
            c.showPage()
            y = 700


def add_OM_info(c, om, dashboard_df, y):
    x = 30
    c.setFont("Helvetica-Bold", 24)
    c.drawString(x, y + 80, om)
    c.setFont("Helvetica", 10)
    for column in COLUMNS_TO_SHOW:
        add_chart(c, om, dashboard_df, column, x, y)
        x += 80


def add_chart(c, om, dashboard_df, column, x, y):
    chart = make_donut(om, column, dashboard_df, actual_expenses)
    column = "zeladoria" if column == "Roçagem e Limpeza Mensal" else column
    chart.save(f"chart{column}{om}.png")
    c.drawString(x, y + 53, column)
    c.drawImage(f"chart{column}{om}.png", x=x, y=y, width=50, height=50)
    os.remove(f"chart{column}{om}.png")
