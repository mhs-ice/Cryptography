from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# --- Padding Functions ---
def pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()

# --- AES Encryption/Decryption ---
def aes_encrypt(plaintext, key, mode_name):
    backend = default_backend()
    iv = os.urandom(16)

    if mode_name == "ECB":
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    elif mode_name == "CBC":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    elif mode_name == "CFB":
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    elif mode_name == "OFB":
        cipher = Cipher(algorithms.AES(key), modes.OFB(iv), backend=backend)
    else:
        raise ValueError("Unsupported mode")

    encryptor = cipher.encryptor()
    padded_data = pad(plaintext.encode())
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext, iv

def aes_decrypt(ciphertext, key, mode_name, iv):
    backend = default_backend()

    if mode_name == "ECB":
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    elif mode_name == "CBC":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    elif mode_name == "CFB":
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    elif mode_name == "OFB":
        cipher = Cipher(algorithms.AES(key), modes.OFB(iv), backend=backend)
    else:
        raise ValueError("Unsupported mode")

    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    try:
        return unpad(padded_plaintext).decode()
    except:
        return padded_plaintext.decode(errors='ignore')  # for stream modes

# --- Main Program ---
def main():
    message = input("Enter plaintext: ")
    key = os.urandom(16)  # 128-bit AES key

    modes_list = ["ECB", "CBC", "CFB", "OFB"]

    for mode in modes_list:
        print(f"\n🔐 Mode: {mode}")
        ciphertext, iv = aes_encrypt(message, key, mode)
        print("Encrypted (hex):", ciphertext.hex())

        decrypted = aes_decrypt(ciphertext, key, mode, iv)
        print("Decrypted:", decrypted)

if __name__ == "__main__":
    main()
