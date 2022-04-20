import pandas as pd
from datetime import datetime

datelist = pd.date_range(datetime.today(), periods=2).tolist()
# print(type(datelist))