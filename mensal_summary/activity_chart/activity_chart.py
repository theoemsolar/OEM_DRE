import io
import matplotlib.pyplot as plt
from reportlab.lib.utils import ImageReader
from mensal_summary.activity_table.activity_table import build_df


def activity_chart(c, dashboard_df, om_data, expenses_data):
    df = build_df(dashboard_df, om_data, expenses_data)

    df.set_index("activity", inplace=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(df))

    predict_color = "#33FF00"
    actual_color = "#FD4B4B"
    excedente_color = "#FF0000"
    ax.bar(x, df["predict"], color=predict_color, label="predict")

    plot_actual(actual_color, ax, df, x)
    plot_overcash(ax, df, excedente_color, x)
    cofigure_axis(ax, df, x)
    configure_borders(ax)
    plot(c)


def plot(c):
    img_buffer = save_images()
    img = ImageReader(img_buffer)
    c.drawImage(img, x=5, y=40, width=550, height=300)


def save_images():
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    return img_buffer


def configure_borders(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")
    plt.tight_layout()


def cofigure_axis(ax, df, x):
    ax.set_xticks(list(x))
    ax.set_xticklabels(df.index)
    ax.set_ylabel("")


def plot_overcash(ax, df, excedente_color, x):
    overflow = (df["actual"] - df["predict"]).clip(lower=0)
    ax.bar(x, overflow, bottom=df["predict"], color=excedente_color, label="Excedente")


def plot_actual(actual_color, ax, df, x):
    actual_within = df["actual"].where(df["actual"] <= df["predict"], df["predict"])
    ax.bar(x, actual_within, color=actual_color, label="actual")
