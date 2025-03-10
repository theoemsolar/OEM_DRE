import streamlit as st
from api.sheet_data import SheetData

from components import TreemapChart, CashFlowDashboard

# st.set_page_config(layout="wide")
if "selected_points" not in st.session_state:
    st.session_state.selected_points = 280


@st.cache_data
def load_data():
    sheet_data = SheetData()
    dashboard_df = sheet_data.get_dashboard_data()
    dashboard_df.rename(columns={dashboard_df.columns[0]: "OM"}, inplace=True)
    om_data = sheet_data.get_OM_datas()
    expenses_data = sheet_data.get_expenses()
    return dashboard_df, om_data, expenses_data


def convert_currency(value):
    if isinstance(value, str):
        value = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(value) if value else 0.0
    return value


dashboard_df, om_data, expenses_data = load_data()

columns_to_convert = dashboard_df.columns[2:]
for col in columns_to_convert:
    if col != "Margem":
        dashboard_df[col] = dashboard_df[col].apply(convert_currency)
om_data["Valor"] = om_data["Valor"].apply(convert_currency)

if __name__ == "__main__":

    TreemapChart(dashboard_df).show()
    # CashFlowDashboard(om_data, expenses_data, dashboard_df).show()
