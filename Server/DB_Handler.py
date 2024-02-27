import sqlite3


def create_table():
    """
    Creates a table 'users' in the database if it doesn't exist already.
    """
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
    """
    Checks if the given password matches the password associated with the given username.

    Parameters:
        username (str): Username of the user.
        given_password (str): Password provided by the user.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
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
    """
    Adds a new user to the database with provided details including past diseases.

    Parameters:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        gender (str): Gender of the user.
        username (str): Unique username of the user.
        password (str): Password of the user.
        past_diseases (str): Past diseases of the user.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO users (first_name,last_name,gender,username, password,past_diseases)
            VALUES (?,?,?,?,?,?);
        """, (first_name, last_name, gender, username, password, past_diseases))

    conn.commit()
    conn.close()


def remove_user(username):
    """
    Removes a user from the database based on the username.

    Parameters:
        username (str): Username of the user to be removed.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
                DELETE FROM users 
                WHERE username = ?;
                """, (username,))

    conn.commit()
    conn.close()


def change_password(username, password):
    """
    Updates the password for a user in the database based on the username.

    Parameters:
        username (str): Username of the user.
        password (str): New password for the user.
    """
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









