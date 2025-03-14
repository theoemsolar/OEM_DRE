import pandas as pd
from dataclasses import dataclass

import streamlit as st

from components.dashboard.calendar import Calendar
from components.dashboard.metrics.metrics import Metrics
from components.dashboard.statement_chart import statement_chart


@dataclass
class Dashboard:
    om_data: pd.DataFrame
    expenses_data: pd.DataFrame
    dashboard_df: pd.DataFrame

    def show(self):
        st.markdown(
            """
            <style>
            .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top:     0rem !important;
                margin-bottom: 0rem !important;
            }

            [class^="css"]  {
                margin: 0px !important;
                padding: 0px !important;
            }

            html, body {
                margin: 0px !important;
                padding: 0px !important;
            }
            
            .calendar {
                padding-top: 6rem !important;
                padding-bottom: 0rem !important;
                margin-top:     0rem !important;
                margin-bottom: 0rem !important;
            }
            .user-select-none{
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top:     0rem !important;
                margin-bottom: 0rem !important;
            }
            .svg-container{
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top:     0rem !important;
                margin-bottom: 0rem !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns([3, 7])
        with col1:
            st.markdown('<div class="metrics">', unsafe_allow_html=True)
            Metrics(self.expenses_data).show()
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="calendar">', unsafe_allow_html=True)
            Calendar(self.om_data, self.expenses_data, self.dashboard_df).show()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sankey_diagram">', unsafe_allow_html=True)
        statement_chart()
        st.markdown("</div>", unsafe_allow_html=True)
