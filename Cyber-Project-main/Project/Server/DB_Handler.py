import sqlite3
from cryptography.fernet import Fernet


def encrypt(data):
    """
    :param data:
    :return: None
    encrypes the data with both encryptions
    """
    data = encrypt_vigenere(data)
    return encrypt_with_fernet(data)

def decrypt(data):
    """
    :param data:
    :return: None
    decrypts the data with both decryptions
    """
    data = decrypt_with_fernet(data)
    return decrypt_vigenere(data)

def encrypt_with_fernet(data):
    """
    :param data:
    :return: encryped data using fernet
    """
    fernet_key = b'2BBSsKejvCFTphbyB2sGtwva6NE4ltdvRpl2-ukOKuA='
    f = Fernet(fernet_key)
    return f.encrypt(data.encode()).decode()

def decrypt_with_fernet(data):
    """
    :param data:
    :return: decrypted data using fernet
    """
    fernet_key = b'2BBSsKejvCFTphbyB2sGtwva6NE4ltdvRpl2-ukOKuA='
    f = Fernet(fernet_key)
    return f.decrypt(data.encode()).decode()

def generate_key(plaintext, key):
    """
    :param plaintext: the text that needs to be encrypted
    :param key: the current key
    :return: a correct key for the plaintext
    """
    key = list(key)
    if len(plaintext) == len(key):
        return key
    else:
        for i in range(len(plaintext) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt_vigenere(plaintext):
    """
    :param plaintext: the text that needs to be encrypted
    :return: encrypted text
    """
    encrypted_text = []
    key = "KJSDLSC"
    key = generate_key(plaintext, key)
    key_index = 0
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            shift = ord(key[key_index]) - ord('A') if key[key_index].isupper() else ord(key[key_index]) - ord('a')
            if plaintext[i].isupper():
                x = (ord(plaintext[i]) - ord('A') + shift) % 26 + ord('A')
            else:
                x = (ord(plaintext[i]) - ord('a') + shift) % 26 + ord('a')
            key_index = (key_index + 1) % len(key)
            encrypted_text.append(chr(x))
        else:
            encrypted_text.append(plaintext[i])
    return "".join(encrypted_text)

def decrypt_vigenere(ciphertext):
    """
    :param ciphertext: ciphered text
    :return: decrypted text using vigenre decryption
    """
    decrypted_text = []
    key = "KJSDLSC"
    key = generate_key(ciphertext, key)
    key_index = 0
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            shift = ord(key[key_index]) - ord('A') if key[key_index].isupper() else ord(key[key_index]) - ord('a')
            if ciphertext[i].isupper():
                x = (ord(ciphertext[i]) - ord('A') - shift + 26) % 26 + ord('A')
            else:
                x = (ord(ciphertext[i]) - ord('a') - shift + 26) % 26 + ord('a')
            key_index = (key_index + 1) % len(key)
            decrypted_text.append(chr(x))
        else:
            decrypted_text.append(ciphertext[i])
    return "".join(decrypted_text)

def create_tables():
    """
    Creates a table 'users' in the database if it doesn't exist already.
    """
    conn = sqlite3.connect(r'../Server/users.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT NOT NULL,
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
    """
    Check whether a user is a doctor or not based on their username.

    Parameters:
        username (str): The username of the user to be checked.

    Returns:
        bool: True if the user is a doctor, False otherwise.
    """
    #checks wheater a user is a doctor or not and returns an answer
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT is_doctor FROM users
        WHERE username=?
        ''', (username,)
    )
    try:
        if cursor.fetchone()[0] == 0:
            return False
        else:
            return True
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
        correct_password = decrypt(cursor.fetchone()[0])


    except TypeError:
        conn.commit()
        conn.close()
        return False

    return correct_password == given_password


def add_user(id, gender, username, password,is_doctor, past_diseases,doctor):
    """
    Adds a new user to the database with provided details including past diseases.

    Parameters:
        username (str): username
        gender (str): Gender of the user.
        username (str): Unique username of the user.
        password (str): Password of the user.
        past_diseases (str): Past diseases of the user.
    """

    past_diseases = past_diseases.replace("[","")
    past_diseases = past_diseases.replace("]", "")
    past_diseases = past_diseases.replace("'","")

    password = encrypt(password)
    past_diseases = encrypt(past_diseases)
    id = encrypt(id)

    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO users (id,gender,username, password,is_doctor,past_diseases,doctor)
            VALUES (?,?,?,?,?,?,?);
        """, (id, gender, username, password,is_doctor,past_diseases,doctor))


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

    password = encrypt(password)
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
        curr_diseases = encrypt(curr_diseases)
        cursor.execute("""
                UPDATE users
                SET past_diseases = ?
                WHERE username = ?;
            """, (curr_diseases, username,))
        print("UPDATED!")

    conn.commit()
    conn.close()

def get_all_doctors():
    """
       Returns a list of all doctors.

       Returns:
           list: A list of usernames of all doctors.
       """
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT username FROM users
        WHERE is_doctor=?
        ''', (1,)
    )
    doctors = []
    for item in cursor.fetchall():
        item = str(item)
        doctors.append(item[2:len(item)-3])

    conn.commit()
    conn.close()

    return doctors

def get_doctor_for_user(username):
    """
        Returns the doctor assigned to a specific user.

        Parameters:
            username (str): The username of the user.

        Returns:
            str: The username of the doctor assigned to the user.
        """
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
    """
       Returns a list of all patients assigned to a specific doctor.

       Parameters:
           doctor (str): The username of the doctor.

       Returns:
           list: A list of usernames of all patients assigned to the doctor.
       """
    conn = sqlite3.connect('../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT username FROM users
        WHERE doctor=?
        ''', (doctor,)
    )

    patients = []
    rows = cursor.fetchall()
    for patient in rows:
        patients.append(patient[0])


    conn.commit()
    conn.close()

    return patients

def get_history_of_diseases(username):
    """
       Retrieves and decrypts the past diseases of a user.

       Parameters:
           username (str): The username of the user.

       Returns:
           list: A list of past diseases of the user.
       """
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
        curr_diseases = cursor.fetchone()[0]
        curr_diseases = decrypt(curr_diseases)
        diseases = list(curr_diseases.split(","))
    except Exception as e:
        print(e)
        return []

    final_diseases = []
    for disease in diseases:
        final_diseases.append(disease[1:])
    conn.commit()
    conn.close()

    return final_diseases

def add_message(sender,receiver,subject,message):
    """
      Adds a message to the database.

      Parameters:
          sender (str): The username of the sender.
          receiver (str): The username of the receiver.
          subject (str): The subject of the message.
          message (str): The content of the message.
      """
    conn = sqlite3.connect(r'../Server/users.db')
    cursor = conn.cursor()


    cursor.execute("""
            INSERT INTO messages (sender,receiver,subject,message)
            VALUES (?,?,?,?);
        """, (sender,receiver,subject,encrypt(message)))

    conn.commit()
    conn.close()


def get_all_messages_for_user(user):
    """
       Retrieves all messages for a specific user and decrypts them.

       Parameters:
           user (str): The username of the user.

       Returns:
           list: A list of dictionaries containing the sender, subject, and decrypted message.
       """
    conn = sqlite3.connect(r'../Server/users.db')
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
        message['message'] = decrypt(message['message'])


    conn.commit()
    conn.close()
    print(all_messages)
    return all_messages

def remove_message(sender , receiver , subject):
    """
       Removes a message from the database.

       Parameters:
           sender (str): The username of the sender.
           receiver (str): The username of the receiver.
           subject (str): The subject of the message.
    """
    conn = sqlite3.connect(r'../Server/users.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM messages WHERE receiver=? AND sender = ? AND subject = ?
        """, (receiver,sender,subject)
    )


    conn.commit()
    conn.close()



