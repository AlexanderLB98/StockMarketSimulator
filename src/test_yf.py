
# from dataAdquisition import get_yf_data
from src.DataAdquisition import DataAdquisition

start_date="2023-01-01"
end_date="2023-09-20"
print(type(end_date))
test = DataAdquisition.get_yf_data(start_date=start_date,end_date= end_date)

print(test)