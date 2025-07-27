import string
import random

def generate_key():
    # Define characters to encrypt: letters, digits, punctuation
    original_chars = string.ascii_letters + string.digits + string.punctuation
    shuffled_chars = list(original_chars)
    random.shuffle(shuffled_chars)
    
    key_map = dict(zip(original_chars, shuffled_chars))
    return key_map

def encrypt(plaintext, key_map):
    result = ""
    for char in plaintext:
        if char in key_map:
            result += key_map[char]
        else:
            result += char  # If any unexpected symbol, leave it as is
    return result

def monoalphabetic_cipher():
    print("===== Extended Monoalphabetic Substitution Cipher =====")
    plaintext = input("Enter plaintext: ")

    key_map = generate_key()

    print("\nSubstitution Key:")
    count = 0
    for k in key_map:
        print(f"{k} -> {key_map[k]}", end="  ")
        count += 1
        if count % 8 == 0:
            print()
    print("\n")

    encrypted = encrypt(plaintext, key_map)
    print("Original Plaintext:", plaintext)
    print("Encrypted Ciphertext:", encrypted)

if __name__ == "__main__":
    monoalphabetic_cipher()
