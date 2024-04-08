import datetime


def change_format(cad: str) -> str:
    date = datetime.datetime.strptime(cad, "%Y-%m-%d").strftime("%d-%m-%Y")
    date_split = date.split("-")
    
    return "-".join([d.lstrip("0") for d in date_split])

def str_to_date(date_str: str) -> datetime.datetime:
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')