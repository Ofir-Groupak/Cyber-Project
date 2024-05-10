import sqlite3
from DB_Handler import *





def encrypt_data(data):
    key = b'2BBSsKejvCFTphbyB2sGtwva6NE4ltdvRpl2-ukOKuA='

    """
    Encrypts the given data using the Fernet encryption algorithm.

    Parameters:
        data (bytes): The data to be encrypted as bytes.
        key (str): The encryption key as a base64 encoded string.

    Returns:
        bytes: The encrypted data.
    """
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    key = b'2BBSsKejvCFTphbyB2sGtwva6NE4ltdvRpl2-ukOKuA='
    """
    Decrypts the given encrypted data using the Fernet encryption algorithm.

    Parameters:
        encrypted_data (bytes): The encrypted data as bytes.
        key (str): The encryption key as a base64 encoded string.

    Returns:
        bytes: The decrypted data.
    """
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()

def create_table():
    """
    Creates a table 'users' in the database if it doesn't exist already.
    """
    conn = sqlite3.connect(r'../Server/messages.db')
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
    conn = sqlite3.connect(r'../Server/messages.db')
    cursor = conn.cursor()


    cursor.execute("""
            INSERT INTO messages (sender,receiver,subject,message)
            VALUES (?,?,?,?);
        """, (sender,receiver,encrypt_data(subject),encrypt_data(message)))

    conn.commit()
    conn.close()


def get_all_messages_for_user(user):

    conn = sqlite3.connect(r'../Server/messages.db')
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

    for message in all_messages:
        message['subject'] = decrypt_data(message['subject'])
        message['message'] = decrypt_data(message['message'])


    conn.commit()
    conn.close()

    return all_messages



if __name__=="__main__":
    create_table()
    # add_message("b","a","hello","nigga")
    # print(get_all_messages_for_user("a"))

