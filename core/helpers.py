import pandas as pd
import datetime


def get_file_name():
    _today = datetime.date.today().strftime("%d-%b-%Y")
    return f"jobs_data_{_today}"


def save_data_to_csv(data: pd.DataFrame):
    file_name = f"{get_file_name()}.csv"
    try:
        data.to_csv(file_name, index=False)
        return data
    except Exception as e:
        raise ValueError(str(e))
