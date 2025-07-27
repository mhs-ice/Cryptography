# Hill Cipher Textbook Implementation in Pure Python

def mod_inverse(a, m):
    """Find modular inverse using Extended Euclidean Algorithm"""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def get_matrix_inverse_2x2(matrix, mod):
    """Find inverse of 2x2 matrix under mod"""
    a, b = matrix[0]
    c, d = matrix[1]
    det = (a * d - b * c) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        raise ValueError("Matrix is not invertible!")

    # Inverse of 2x2 matrix: (1/det) * [d -b; -c a]
    inv_matrix = [
        [(d * det_inv) % mod, (-b * det_inv) % mod],
        [(-c * det_inv) % mod, (a * det_inv) % mod]
    ]
    return inv_matrix

def text_to_numbers(text):
    return [ord(char.upper()) - ord('A') for char in text]

def numbers_to_text(numbers):
    return ''.join([chr((num % 26) + ord('A')) for num in numbers])

def chunk_text(text, size):
    if len(text) % size != 0:
        text += 'X' * (size - len(text) % size)  # Padding
    return [text[i:i+size] for i in range(0, len(text), size)]

def multiply_matrix_vector(matrix, vector, mod):
    result = []
    for row in matrix:
        total = sum([row[i] * vector[i] for i in range(len(vector))])
        result.append(total % mod)
    return result

def hill_encrypt(plaintext, key_matrix):
    plaintext = plaintext.replace(" ", "").upper()
    chunks = chunk_text(plaintext, len(key_matrix))
    result = []
    for chunk in chunks:
        vector = text_to_numbers(chunk)
        encrypted_vector = multiply_matrix_vector(key_matrix, vector, 26)
        result.extend(encrypted_vector)
    return numbers_to_text(result)

def hill_decrypt(ciphertext, key_matrix):
    inverse_matrix = get_matrix_inverse_2x2(key_matrix, 26)
    chunks = chunk_text(ciphertext, len(key_matrix))
    result = []
    for chunk in chunks:
        vector = text_to_numbers(chunk)
        decrypted_vector = multiply_matrix_vector(inverse_matrix, vector, 26)
        result.extend(decrypted_vector)
    return numbers_to_text(result)

# ---- Menu for User ----
print("Hill Cipher Program")
print("E/e: Encryption")
print("D/d: Decryption")
choice = input("Enter your choice: ").strip().lower()

# Example 2x2 key matrix (must be invertible mod 26)
key_matrix = [
    [3, 3],
    [2, 5]
]

if choice == 'e':
    plaintext = input("Enter plaintext: ").strip()
    ciphertext = hill_encrypt(plaintext, key_matrix)
    print("\nPlaintext : ", plaintext.upper())
    print("Ciphertext: ", ciphertext)

elif choice == 'd':
    ciphertext = input("Enter ciphertext: ").strip()
    plaintext = hill_decrypt(ciphertext, key_matrix)
    print("\nCiphertext: ", ciphertext.upper())
    print("Decrypted : ", plaintext)

else:
    print("Invalid choice!")
