def encrypt_caesar(text, shift):
    result = ""
    for char in text:
        if 32 <= ord(char) <= 126:
            # Shift within printable ASCII range (32-126)
            shifted = (ord(char) - 32 + shift) % 95 + 32
            result += chr(shifted)
        else:
            # Leave characters outside 32-126 unchanged (e.g., newline, tab)
            result += char
    return result

def decrypt_caesar(text, shift):
    # Decrypt is just encrypt with negative shift
    return encrypt_caesar(text, -shift)

# Read from input file
with open('text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Get cipher key
shift = int(input("Enter the cipher key (integer shift): "))

# Encrypt
encrypted = encrypt_caesar(text, shift)

# Write encrypted text to another file
with open('cipher.txt', 'w', encoding='utf-8') as cipher_file:
    cipher_file.write(encrypted)

print("\nEncrypted message:")
print(encrypted)

# Decrypt
decrypted = decrypt_caesar(encrypted, shift)
print("\nDecrypted message:")
print(decrypted)
