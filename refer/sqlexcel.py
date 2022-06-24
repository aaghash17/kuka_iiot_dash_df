import sys
import pyodbc as odbc
import pandas as pd


DRIVER = 'SQL Server'
SERVER_NAME = 'DESKTOP-1AVGRC3'
DATABASE_NAME = 'KUKA'

conn_string = f"""
    Driver={{{DRIVER}}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    conn = odbc.connect(conn_string)
    print('CONNECTED TO DB')
except Exception as e:
    print(e)
    print('CONNECTION TERMINTED')
    sys.exit()
else:
    cursor = conn.cursor()

sql_query = pd.read_sql_query(''' 
                              select * from [KUKA].[dbo].[Table_1]
                              '''
                              ,conn) # here, the 'conn' is the variable that contains your database connection information from step 2

df = pd.DataFrame(sql_query)

try:
    df.to_csv (r'C:\Users\DRAPLMHS5\Desktop\exported_data.csv', index = False) # place 'r' before the path name
    print('EXPORT COMPLETED')
except Exception as e:
    print(e)
    print('EXPORT ERROR')
    sys.exit()
else:
    print('DO NO')
    
