import streamlit as st
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib.colors import blue, Color

image_path = "images/white-logo.png"


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def header(c):
    rectangle_metrics = add_rectangle(c)
    add_month_title(c, rectangle_metrics)
    add_week_range(c, rectangle_metrics)
    add_logo(c, rectangle_metrics)


def add_rectangle(c):
    page_length, page_height = A4
    rectangle_length = page_length
    rectangle_height = 103
    rectangle_x = 0
    rectangle_y = page_height - rectangle_height
    rgb_color = hex_to_rgb("00559B")

    c.setFillColorRGB(*rgb_color)
    c.rect(rectangle_x, rectangle_y, rectangle_length, rectangle_height, fill=1)
    return rectangle_x, rectangle_y, rectangle_length, rectangle_height


def add_month_title(c, rectangle_metrics):
    rectangle_x, rectangle_y, rectangle_length, rectangle_height = rectangle_metrics
    c.setFont("Helvetica-Bold", 40)
    text_x = rectangle_x + rectangle_length / 2
    text_y = rectangle_y + rectangle_height / 2 - 8
    c.setFillColorRGB(1, 1, 1)
    c.drawCentredString(text_x, text_y, "Fevereiro")


def add_week_range(c, rectangle_metrics):
    rectangle_x, rectangle_y, rectangle_length, rectangle_height = rectangle_metrics
    c.setFont("Helvetica-Bold", 12)
    text_x = rectangle_x + rectangle_length / 2
    text_y = rectangle_y + rectangle_height / 2 - 30
    c.setFillColorRGB(1, 1, 1)
    c.drawCentredString(text_x, text_y, "02/02/2025 - 01/03/2025")


def add_logo(c, rectangle_metrics):
    rectangle_x, rectangle_y, rectangle_length, rectangle_height = rectangle_metrics

    image_width = 124
    image_height = 53
    image_x = 0
    image_y = rectangle_y + (rectangle_height - image_height) / 2
    c.drawImage(
        image_path,
        image_x,
        image_y,
        width=image_width,
        height=image_height,
        mask="auto",
    )
