import sqlite3


def create_table():
    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        past_diseases TEXT NOT NULL
    );

    """)

    conn.commit()
    conn.close()


def check_password(username, given_password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT password FROM users
        WHERE username=?
        ''', (username,)
    )
    try:
        correct_password = cursor.fetchone()[0]
    except TypeError:
        conn.commit()
        conn.close()

        return False

    conn.commit()
    conn.close()

    return correct_password == given_password


def add_user(first_name, last_name, gender, username, password, past_diseases):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO users (first_name,last_name,gender,username, password,past_diseases)
            VALUES (?,?,?,?,?,?);
        """, (first_name, last_name, gender, username, password, past_diseases))

    conn.commit()
    conn.close()


def remove_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
                DELETE FROM users 
                WHERE username = ?;
                """, (username,));

    conn.commit()
    conn.close()


def change_password(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE username = ?;
            """, (password, username))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    add_user('moshe', 'moshe', 'male', 'admin', '1234', 'None')
    # print(check_password('admin' ,'12345'))
    # remove_user('admin')
    # change_password('admin1','admin')









