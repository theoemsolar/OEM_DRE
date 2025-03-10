from api.sheet_data import SheetData
import random


def convert_currency(value):
    if isinstance(value, str):
        value = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(value) if value else 0.0
    return value


def main():
    sheet_data = SheetData()

    oms_df = sheet_data.get_OM_datas()
    expenses = sheet_data.get_dashboard_data()
    merged_df = oms_df.merge(expenses, how="left", on="OM")

    all_data = {}

    for om in merged_df["OM"]:
        category_dict = {}
        for category in expenses.columns[2:8]:
            category_dict[category] = (
                convert_currency(merged_df[merged_df["OM"] == om][category].tolist()[0])
                * random.randint(0, 20)
                / 10.0
            )
        all_data[om] = category_dict

    print(all_data)


if __name__ == "__main__":
    main()
