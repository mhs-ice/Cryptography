def caesar_decrypt(cipher_text, key):
    decrypted_text = ""
    for char in cipher_text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            decrypted_text += chr((ord(char) - base - key) % 26 + base)
        else:
            decrypted_text += char
    return decrypted_text

def brute_force_caesar(cipher_text):
    print("Brute Force Results for Caesar Cipher:")
    for key in range(1, 26):  # Try all 25 possible keys
        decrypted = caesar_decrypt(cipher_text, key)
        print(f"Key #{key:2d}: {decrypted}")

# Example ciphertext (encrypted using Caesar cipher)
cipher_text = "Wklv lv d ehdxwlixo gdcb!"
brute_force_caesar(cipher_text)
