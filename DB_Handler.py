import sqlite3

conn = sqlite3.connect('users.db')

cursor = conn.cursor()

cursor.execute( '''
CREATE TABLE IF NOT EXISTS my_table (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
);
'''
)

conn.commit()
conn.close()

