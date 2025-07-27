import string

def generate_key_matrix(key):
    # Remove duplicates and replace J with I
    key = key.upper().replace('J', 'I')
    seen = set()
    key_string = ""
    for char in key:
        if char in string.ascii_uppercase and char not in seen:
            seen.add(char)
            key_string += char
    
    # Add remaining letters (except J) to the key string
    for char in string.ascii_uppercase:
        if char != 'J' and char not in seen:
            key_string += char

    # Create 5x5 matrix
    matrix = [list(key_string[i:i+5]) for i in range(0, 25, 5)]
    return matrix

def find_position(matrix, char):
    for row_idx, row in enumerate(matrix):
        if char in row:
            return row_idx, row.index(char)
    return None

def prepare_text(text, for_encryption=True):
    text = text.upper().replace('J', 'I')
    text = ''.join([c for c in text if c in string.ascii_uppercase])

    prepared = ""
    i = 0
    while i < len(text):
        char1 = text[i]
        if i + 1 < len(text):
            char2 = text[i+1]
            if char1 == char2:
                prepared += char1 + 'X'
                i += 1
            else:
                prepared += char1 + char2
                i += 2
        else:
            prepared += char1 + 'X'
            i += 1

    return prepared

def playfair_encrypt(plaintext, key):
    matrix = generate_key_matrix(key)
    prepared_text = prepare_text(plaintext)

    ciphertext = ""
    for i in range(0, len(prepared_text), 2):
        r1, c1 = find_position(matrix, prepared_text[i])
        r2, c2 = find_position(matrix, prepared_text[i+1])

        if r1 == r2:
            ciphertext += matrix[r1][(c1 + 1) % 5]
            ciphertext += matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            ciphertext += matrix[(r1 + 1) % 5][c1]
            ciphertext += matrix[(r2 + 1) % 5][c2]
        else:
            ciphertext += matrix[r1][c2]
            ciphertext += matrix[r2][c1]

    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = generate_key_matrix(key)

    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        r1, c1 = find_position(matrix, ciphertext[i])
        r2, c2 = find_position(matrix, ciphertext[i+1])

        if r1 == r2:
            plaintext += matrix[r1][(c1 - 1) % 5]
            plaintext += matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            plaintext += matrix[(r1 - 1) % 5][c1]
            plaintext += matrix[(r2 - 1) % 5][c2]
        else:
            plaintext += matrix[r1][c2]
            plaintext += matrix[r2][c1]

    # Optional: remove trailing 'X' added during encryption if it looks like padding
    return plaintext

# Example usage
plaintext = input("Enter your Message : ")
key = input("Enter your key : ")

print("Key Matrix:")
matrix = generate_key_matrix(key)
for row in matrix:
    print(row)

encrypted = playfair_encrypt(plaintext, key)
print("\nEncrypted Text:", encrypted)

decrypted = playfair_decrypt(encrypted, key)
print("Decrypted Text:", decrypted)
