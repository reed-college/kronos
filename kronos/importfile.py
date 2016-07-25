from sqlalchemy import create_engine
import pandas as pd

# Remember to change user name and file path.
engine = create_engine('postgresql://Jiahui:pass@localhost/db_kronos')

# Import CSV files

# (Problem: For some reason dates will be saved as text when converted to CSV from Excel, 
# hence they cannot be appended to the event table.)

# df_csv = pd.read_csv('/Users/Jiahui/kronos/kronos/csvdata.csv')
# df_csv.to_sql('pandas', engine, if_exists='append')

# assert df_csv.query('dtstart > dtend').empty

# Import Excel files
df_xlsx = pd.read_excel('/Users/Jiahui/kronos/kronos/exceldata.xlsx')
df_xlsx.to_sql('event', engine, if_exists='append', index=False)

assert df_xlsx.query('dtstart > dtend').empty

# Append data from Excel to the event table.
# pd.read_sql_query('INSERT INTO event (summary, dtstart, dtend, private, userid) SELECT summary, dtstart, dtend, private, userid FROM pandas;', engine)
    