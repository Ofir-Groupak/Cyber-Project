import sqlite3

conn = sqlite3.connect('users.db')

cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
'''

cursor.execute(create_table_query)

conn.commit()
conn.close()


