# Elliptic Curve: y^2 = x^3 + ax + b over field mod p
a = 1
b = 6
p = 11  # Prime number for finite field

# Define elliptic curve point addition
def inverse_mod(k, p):
    """Returns the inverse of k modulo p."""
    return pow(k, -1, p)

def point_add(P, Q):
    """Adds two points P and Q on the elliptic curve."""
    if P == 'O':
        return Q
    if Q == 'O':
        return P
    if P == Q:
        m = (3 * P[0]**2 + a) * inverse_mod(2 * P[1], p) % p
    else:
        m = (Q[1] - P[1]) * inverse_mod(Q[0] - P[0], p) % p

    x_r = (m**2 - P[0] - Q[0]) % p
    y_r = (m * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)

# Scalar multiplication (n * P)
def scalar_mult(k, P):
    """Multiplies point P by scalar k using double-and-add algorithm."""
    result = 'O'
    current = P
    while k > 0:
        if k % 2 == 1:
            result = point_add(result, current)
        current = point_add(current, current)
        k = k // 2
    return result

# ECC Encryption
def ecc_encrypt(points, public_key, G):
    """Encrypts list of points using ECC."""
    ciphertext = []
    k = 5  # Fixed random number (for demo; should be random in practice)

    # Compute k*G (point to send)
    kG = scalar_mult(k, G)

    # Compute k*public_key (shared secret)
    kP = scalar_mult(k, public_key)

    # Encrypt each point: C = M + kP
    for M in points:
        if kP != 'O':
            encrypted_point = point_add(M, kP)
        else:
            encrypted_point = M
        ciphertext.append(encrypted_point)

    return (kG, ciphertext)

# ECC Decryption
def ecc_decrypt(ciphertext, private_key):
    """Decrypts ciphertext using ECC."""
    kG, encrypted_points = ciphertext
    plaintext_points = []

    # Compute private_key * kG (which equals kP)
    kP = scalar_mult(private_key, kG)

    # For each encrypted point, subtract kP to get original point
    for point in encrypted_points:
        if kP != 'O':
            minus_kP = (kP[0], (-kP[1]) % p)
            decrypted_point = point_add(point, minus_kP)
        else:
            decrypted_point = point
        plaintext_points.append(decrypted_point)

    return plaintext_points

# Helper: parse points input from string like "(2,7),(5,9),..."
def parse_points(input_str):
    points = []
    pairs = input_str.strip().split('),')
    for pair in pairs:
        pair = pair.replace('(', '').replace(')', '').strip()
        if not pair:
            continue
        x_str, y_str = pair.split(',')
        points.append((int(x_str), int(y_str)))
    return points

# --- Main demo ---
if __name__ == "__main__":
    G = (2, 7)
    private_A = 3
    public_A = scalar_mult(private_A, G)

    private_B = 7
    public_B = scalar_mult(private_B, G)

    print("Public key of Alice:", public_A)
    print("Public key of Bob:", public_B)
    print("Shared secret Alice:", scalar_mult(private_A, public_B))
    print("Shared secret Bob:", scalar_mult(private_B, public_A))

    # User inputs points to encrypt (instead of text)
    inp = input("\nEnter points to encrypt as (x,y): ")
    points_to_encrypt = parse_points(inp)

    ciphertext = ecc_encrypt(points_to_encrypt, public_A, G)
    print("\nCiphertext:")
    #print("kG =", ciphertext[0])
    print("Encrypted Points:")
    for pt in ciphertext[1]:
        print(pt)

    decrypted_points = ecc_decrypt(ciphertext, private_A)
    print("\nDecrypted Points:")
    for pt in decrypted_points:
        print(pt)
