import locale
import datetime
from scripts.oCelulas import DataCelulas
import pandas as pd

today = datetime.datetime.now()
fechas = pd.DataFrame(pd.date_range(start='2024-09-01', end='2024-09-24', freq='D'), columns=['fecha_base'])
print(fechas)