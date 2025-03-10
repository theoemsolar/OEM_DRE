from .treemap_chart.treemap_chat import TreemapChart
from .dashboard.dashboard import Dashboard
import streamlit as st
import datetime

if "current_week" not in st.session_state:
    st.session_state.current_week = datetime.date.today()

from .cash_flow import CashFlowDashboard
