from sqlalchemy import create_engine
import pandas as pd

# Remember to change user name and file path.
engine = create_engine('postgresql://Jiahui:pass@localhost/db_kronos')

# Import CSV files
df_csv = pd.read_csv('/Users/Jiahui/kronos/kronos/csvdata.csv')
df_csv.to_sql('pandas_db', engine, if_exists='append')

assert df_csv.query('dtstart > dtend').empty

# Import Excel files
df_xlsx = pd.read_excel('/Users/Jiahui/kronos/kronos/exceldata.xlsx')
df_xlsx.to_sql('pandas_db', engine, if_exists='append')

assert df_xlsx.query('dtstart > dtend').empty
