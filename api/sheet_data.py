import os
import json
import gspread
import datetime
import pandas as pd
from dotenv import load_dotenv
from dataclasses import dataclass, field
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

credentials_str = os.getenv("DATA_SHEET_CREDENTIALS", None)
if credentials_str:
    credentials_json = json.loads(credentials_str)
else:
    raise ValueError("Erro ao carregar oas credenciais")


SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, SCOPE)
client = gspread.authorize(credentials)

spreadsheet_name = "DRE"


@dataclass
class SheetData:
    dashboard_data: client = field(init=False)
    om_data: client = field(init=False)

    def __post_init__(self):
        self.om_data = client.open(spreadsheet_name).worksheet("Página1")
        self.expenses_data = client.open(spreadsheet_name).worksheet("Custo")
        self.dashboard_data = client.open(spreadsheet_name).worksheet("Dashboard")

    def get_dashboard_data(self):
        print(f"{datetime.datetime.now()} - request dashboard data")
        return pd.DataFrame(self.dashboard_data.get_all_records())

    def get_OM_datas(self):
        print(f"{datetime.datetime.now()} - request OM data")

        df = pd.DataFrame(self.om_data.get_all_records())
        return df

    def get_expenses(self):
        print(f"{datetime.datetime.now()} - request expenses data")

        return pd.DataFrame(self.expenses_data.get_all_records())[
            [
                "data da Roçagem e Limpeza Mensal",
                "data da Custo OP",
                "data da Comissão",
                "data da Folha ADM",
                "data da Imposto",
                "data da Bancagem",
                "data da Custo Fixo",
            ]
        ]
