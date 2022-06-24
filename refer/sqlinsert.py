import sys
import pyodbc as odbc

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


insert_statement = """
    INSERT INTO [dbo].[Table_1]
    VALUES (?)
"""

record = ['x']


try:
    print(record)
    cursor.execute(insert_statement, record)        
except Exception as e:
    cursor.rollback()
    print(e.value)
    print('ROLLED BACK')
else:
    print('RECORD INSERTED')
    cursor.commit()
    cursor.close()


finally:
    if conn.connected == 1:
        print('CONNECTION CLOSED')
        conn.close()
