import pymysql
try:
    db_connection=pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='Silverus',
    password='Sql320652548!',
    database='tg_bot',
    cursorclass=pymysql.cursors.DictCursor
    )
    print("\nDatabase connection successful!")
except Exception as ex:
    print("\nConnection failed...")
    print(ex,'\n')


import sqlite3
db_history = sqlite3.connect('history.db')
history_cursor = db_history.cursor()
history_cursor.execute("""CREATE TABLE IF NOT EXISTS "command_line_history" (
                            "id"	INTEGER NOT NULL,
                            "chat_id"	INTEGER,
                            "user"	NUMERIC,
                            "command"	TEXT,
                            "time"	TEXT,
                            PRIMARY KEY("id" AUTOINCREMENT)
                            );"""
                       )


db_history.commit()
