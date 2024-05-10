from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a new Fernet key and returns it as a base64 encoded string.
    """
    key = Fernet.generate_key()
    return key

def encrypt_data(data, key):
    """
    Encrypts the given data using the Fernet encryption algorithm.

    Parameters:
        data (bytes): The data to be encrypted as bytes.
        key (str): The encryption key as a base64 encoded string.

    Returns:
        bytes: The encrypted data.
    """
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return encrypted_data

def decrypt_data(encrypted_data, key):
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
    return decrypted_data

# Example usage:
if __name__ == "__main__":
    # Generate a new encryption key
    key = b'2BBSsKejvCFTphbyB2sGtwva6NE4ltdvRpl2-ukOKuA='
    print("Encryption Key:", key)

    # Data to be encrypted
    data = b"Hello, this is a secret message!"

    # Encrypt data
    encrypted_data = encrypt_data(data, key)
    print("Encrypted Data:", encrypted_data)

    # Decrypt data
    decrypted_data = decrypt_data(encrypted_data, key)
    print("Decrypted Data:", decrypted_data.decode())
