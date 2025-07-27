# Convert letter to number (A=0 to Z=25)
def char_to_num(c):
    return ord(c.upper()) - ord('A')

# Convert number to letter
def num_to_char(n):
    return chr((n % 26) + ord('A'))

# Prepare text: remove spaces, uppercase, pad with X
def prepare_text(text, size):
    text = text.replace(" ", "").upper()
    if len(text) % size != 0:
        text += 'X' * (size - len(text) % size)
    return text

# Modular inverse (brute-force method)
def modinv(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("No modular inverse exists for determinant")

# Multiply 2x2 matrix with 2x1 vector modulo 26
def matrix_vector_multiply(matrix, vector):
    result = [0, 0]
    result[0] = (matrix[0][0]*vector[0] + matrix[0][1]*vector[1]) % 26
    result[1] = (matrix[1][0]*vector[0] + matrix[1][1]*vector[1]) % 26
    return result

# Inverse of a 2x2 matrix mod 26
def inverse_key_matrix(matrix):
    # Calculate determinant
    det = (matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]) % 26
    det_inv = modinv(det, 26)

    # Adjugate matrix
    inv_matrix = [
        [ matrix[1][1] * det_inv % 26, -matrix[0][1] * det_inv % 26],
        [-matrix[1][0] * det_inv % 26,  matrix[0][0] * det_inv % 26]
    ]

    # Make sure all values are positive mod 26
    for i in range(2):
        for j in range(2):
            inv_matrix[i][j] = inv_matrix[i][j] % 26

    return inv_matrix

# Hill cipher encryption
def hill_encrypt(plaintext, key_matrix):
    plaintext = prepare_text(plaintext, 2)
    ciphertext = ""

    for i in range(0, len(plaintext), 2):
        block = plaintext[i:i+2]
        vector = [char_to_num(block[0]), char_to_num(block[1])]
        result = matrix_vector_multiply(key_matrix, vector)
        ciphertext += ''.join(num_to_char(n) for n in result)

    return ciphertext

# Hill cipher decryption
def hill_decrypt(ciphertext, key_matrix):
    inv_matrix = inverse_key_matrix(key_matrix)
    decrypted_text = ""

    for i in range(0, len(ciphertext), 2):
        block = ciphertext[i:i+2]
        vector = [char_to_num(block[0]), char_to_num(block[1])]
        result = matrix_vector_multiply(inv_matrix, vector)
        decrypted_text += ''.join(num_to_char(n) for n in result)

    return decrypted_text

# Define 2x2 invertible key matrix mod 26
key_matrix = [
    [3, 3],
    [2, 5]
]

# Validate matrix determinant
det = (key_matrix[0][0]*key_matrix[1][1] - key_matrix[0][1]*key_matrix[1][0]) % 26
try:
    modinv(det, 26)
except ValueError:
    print("❌ Invalid key matrix. Determinant must be coprime with 26.")
    exit()

# Run encryption and decryption
plaintext = input("Enter the plaintext: ")
ciphertext = hill_encrypt(plaintext, key_matrix)
print("🔒 Encrypted text:", ciphertext)

decrypted = hill_decrypt(ciphertext, key_matrix)
print("🔓 Decrypted text:", decrypted)
