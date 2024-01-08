import sqlite3

def create_table():
    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );
    
    """)

    conn.commit()
    conn.close()

def check_password(username , given_password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT password FROM users
        WHERE username=?
        ''',(username,)
    )
    correct_password = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return correct_password == given_password
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?);
        """,(username, password))

    conn.commit()
    conn.close()

def remove_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
                DELETE FROM users 
                WHERE username = ?;
                """,(username,));

    conn.commit()
    conn.close()

def change_password(username , password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE username = ?;
            """, (password,username))

    conn.commit()
    conn.close()





if __name__=="__main__":
    create_table()
    #add_user('admin','1234')
    #print(check_password('admin' ,'12345'))
    #remove_user('admin')
    #change_password('admin1','admin')









