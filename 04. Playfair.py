def prepare_input(text):
    # Convert to uppercase and remove non-letters
    text = ''.join(filter(str.isalpha, text.upper()))

    # Replace J with I
    text = text.replace('J', 'I')

    # Create digraphs (pairs)
    i = 0
    digraphs = []
    while i < len(text):
        a = text[i]
        b = ''
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2
        else:
            b = 'X'
            i += 1
        digraphs.append(a + b)
    return digraphs

def create_matrix(key):
    # Remove duplicates and replace J with I
    key = key.upper().replace('J', 'I')
    seen = set()
    matrix = []

    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)

    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    return [matrix[i*5:(i+1)*5] for i in range(5)]

def find_position(matrix, letter):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == letter:
                return i, j
    return None

def encrypt_pair(pair, matrix):
    a_row, a_col = find_position(matrix, pair[0])
    b_row, b_col = find_position(matrix, pair[1])

    if a_row == b_row:
        return matrix[a_row][(a_col + 1) % 5] + matrix[b_row][(b_col + 1) % 5]
    elif a_col == b_col:
        return matrix[(a_row + 1) % 5][a_col] + matrix[(b_row + 1) % 5][b_col]
    else:
        return matrix[a_row][b_col] + matrix[b_row][a_col]

def decrypt_pair(pair, matrix):
    a_row, a_col = find_position(matrix, pair[0])
    b_row, b_col = find_position(matrix, pair[1])

    if a_row == b_row:
        return matrix[a_row][(a_col - 1) % 5] + matrix[b_row][(b_col - 1) % 5]
    elif a_col == b_col:
        return matrix[(a_row - 1) % 5][a_col] + matrix[(b_row - 1) % 5][b_col]
    else:
        return matrix[a_row][b_col] + matrix[b_row][a_col]

def playfair_encrypt(plaintext, key):
    matrix = create_matrix(key)
    digraphs = prepare_input(plaintext)
    return ''.join([encrypt_pair(pair, matrix) for pair in digraphs])

def playfair_decrypt(ciphertext, key):
    matrix = create_matrix(key)
    digraphs = prepare_input(ciphertext)
    return ''.join([decrypt_pair(pair, matrix) for pair in digraphs])

# ---------- Example Usage ----------
if __name__ == "__main__":
    key = input("Enter the key: ")
    text = input("Enter the plaintext: ")

    encrypted = playfair_encrypt(text, key)
    print(f"Encrypted: {encrypted}")

    decrypted = playfair_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
