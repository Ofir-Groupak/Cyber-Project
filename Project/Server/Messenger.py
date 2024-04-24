import sqlite3
from DB_Handler import *
def create_table():
    """
    Creates a table 'users' in the database if it doesn't exist already.
    """
    conn = sqlite3.connect(r'C:\Users\Ofir\PycharmProjects\Cyber-Project2\Project\Server\messages.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        sender TEXT NOT NULL,
        receiver last_name TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def add_message(sender,receiver,subject,message):
    conn = sqlite3.connect(r'C:\Users\Ofir\PycharmProjects\Cyber-Project2\Project\Server\messages.db')
    cursor = conn.cursor()


    cursor.execute("""
            INSERT INTO messages (sender,receiver,subject,message)
            VALUES (?,?,?,?);
        """, (sender,receiver,subject,message))

    conn.commit()
    conn.close()


def get_all_messages_for_user(user):

    conn = sqlite3.connect(r'C:\Users\Ofir\PycharmProjects\Cyber-Project2\Project\Server\messages.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT sender,subject,message FROM messages WHERE receiver=?
        """,(user,)
    )
    all_messages = []
    message_pattern = ["sender","subject","message"]
    for message in cursor.fetchall():
        all_messages.append(dict(zip(message_pattern,message)))


    conn.commit()
    conn.close()

    return all_messages

def get_most_available_doctor():


if __name__=="__main__":
    create_table()
    add_message("moshe","admin","hello","nigga")
    get_all_messages_for_user("moshe")