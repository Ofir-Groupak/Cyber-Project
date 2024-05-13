import sqlite3
from cryptography.fernet import Fernet







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


def create_tables():
    """
    Creates a table 'users' in the database if it doesn't exist already.
    """
    conn = sqlite3.connect(r'../Server/users.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        is_doctor BOOLEAN NOT NULL,
        past_diseases TEXT NOT NULL,
        doctor TEXT NOT NULL
    );
    """)

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

def is_doctor(username):
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT is_doctor FROM users
        WHERE username=?
        ''', (username,)
    )
    try:
        return cursor.fetchone()[0]
    except TypeError:
        return False
    return False

def check_password(username, given_password):
    """
    Checks if the given password matches the password associated with the given username.

    Parameters:
        username (str): Username of the user.
        given_password (str): Password provided by the user.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT password FROM users
        WHERE username=?
        ''', (username,)
    )


    try:
        correct_password = decrypt_data(cursor.fetchone()[0])


    except TypeError:
        conn.commit()
        conn.close()
        return False

    return correct_password == given_password


def add_user(first_name, last_name, gender, username, password,is_doctor, past_diseases,doctor):
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

    past_diseases = past_diseases.replace("[","")
    past_diseases = past_diseases.replace("]", "")
    past_diseases = past_diseases.replace("'","")

    password = encrypt_data(password)
    past_diseases = encrypt_data(past_diseases)
    first_name = encrypt_data(first_name)
    last_name = encrypt_data(last_name)

    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO users (first_name,last_name,gender,username, password,is_doctor,past_diseases,doctor)
            VALUES (?,?,?,?,?,?,?,?);
        """, (first_name, last_name, gender, username, password,is_doctor,past_diseases,doctor))


    #add_disease(username)
    conn.commit()
    conn.close()


def remove_user(username):
    """
    Removes a user from the database based on the username.

    Parameters:
        username (str): Username of the user to be removed.
    """
    conn = sqlite3.connect('../Server/users.db')
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
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    password = encrypt_data(password)
    cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE username = ?;
            """, (password, username))

    conn.commit()
    conn.close()

def add_disease(username, disease):
    """
    Adds a disease to a user based on their username.

    Parameters:
        username (str): Username of the user.
        disease (str): Disease to be added to the user.
    """
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute("""
                SELECT past_diseases FROM users
                WHERE username = ?;
            """, (username,))
    curr_diseases = get_history_of_diseases(username)
    print('a',curr_diseases)


    if disease not in curr_diseases:
        curr_diseases.append(disease)
        curr_diseases = str(curr_diseases)
        curr_diseases = curr_diseases.replace("[", "")
        curr_diseases = curr_diseases.replace("]", "")
        curr_diseases = curr_diseases.replace("'", "")
        curr_diseases = encrypt_data(curr_diseases)
        cursor.execute("""
                UPDATE users
                SET past_diseases = ?
                WHERE username = ?;
            """, (curr_diseases, username,))
        print("UPDATED!")

    conn.commit()
    conn.close()

def get_all_doctors():
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT username FROM users
        WHERE is_doctor=?
        ''', ("True",)
    )
    doctors = []
    for item in cursor.fetchall():
        item = str(item)
        doctors.append(item[2:len(item)-3])

    conn.commit()
    conn.close()

    return doctors

def get_doctor_for_user(username):
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT doctor FROM users
        WHERE username=?
        ''',(username,)
    )

    doctor = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return doctor


def get_all_patients(doctor):
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT username FROM users
        WHERE doctor=?
        ''', (doctor,)
    )

    patients = []
    for patient in cursor.fetchall():
        patients.append(patient[0])


    conn.commit()
    conn.close()

    return patients

def get_history_of_diseases(username):
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT past_diseases FROM users
        WHERE username=?
        ''', (username,)
    )
    diseases = []
    try:
        curr_diseases = cursor.fetchone()[0].decode()
        curr_diseases = decrypt_data(curr_diseases)
        diseases = list(curr_diseases.split(","))
    except TypeError:
        return []

    conn.commit()
    conn.close()

    return diseases

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


if __name__ == "__main__":
    create_tables()
    add_user('e', 'e', 'Male', 'Doctor', '123',"True", str(['Heart attack']),'a')
    #print(is_doctor("admin1"))
    # print(check_password('admin' ,'12345'))
    #remove_user('Doctor')
    # change_password('admin1','admin')
    #print(get_all_doctors())
    #print(get_all_patients('doc'))
    #print(check_password('doc','doc'))
    #add_disease('a','Common Cold')
    #print(get_history_of_diseases('a'))






