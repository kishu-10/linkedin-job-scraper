import pandas as pd
import datetime


def get_file_name():
    _today = datetime.date.today().strftime("%d-%b-%Y")
    return f"jobs_data_{_today}"


def save_data_to_csv(data: list, file_name=None):
    file_name = f"{get_file_name()}.csv"
    try:
        dataframe = pd.DataFrame.from_dict(data)
        dataframe.to_csv(file_name, index=False)
        return dataframe
    except Exception as e:
        raise ValueError(str(e))
