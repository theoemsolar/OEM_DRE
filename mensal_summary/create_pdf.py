import streamlit as st

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from mensal_summary.header import header
from mensal_summary.OMs_summary import oms_summary
from mensal_summary.month_metrics import month_metrics
from mensal_summary.activity_table import activity_table
from mensal_summary.activity_chart import activity_chart

PDF_PATH = "relatorio_mensal.pdf"


def create_pdf(dashboard_df, om_data, expenses_data):
    c = canvas.Canvas(PDF_PATH, pagesize=A4)
    header(c)
    month_metrics(c, dashboard_df, om_data, expenses_data)
    activity_table(c, dashboard_df, om_data, expenses_data)
    activity_chart(c, dashboard_df, om_data, expenses_data)
    c.showPage()
    oms_summary(c, dashboard_df, om_data, expenses_data)

    c.save()
