# Elliptic Curve: y^2 = x^3 + ax + b over field mod p
a = 1
b = 6
p = 11  # Prime number for finite field

def inverse_mod(k, p):
    """Returns the inverse of k modulo p using pow()."""
    return pow(k, -1, p)

def point_add(P, Q):
    """Adds two points P and Q on the elliptic curve."""
    if P == 'O': return Q
    if Q == 'O': return P
    if P[0] == Q[0] and (P[1] != Q[1] or P[1] == 0): return 'O'  # Point at infinity

    if P == Q:
        m = (3 * P[0]**2 + a) * inverse_mod(2 * P[1], p) % p
    else:
        m = (Q[1] - P[1]) * inverse_mod(Q[0] - P[0], p) % p

    x_r = (m**2 - P[0] - Q[0]) % p
    y_r = (m * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)

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

def ecc_encrypt(points, public_key, G, k):
    """Encrypts list of points using ECC."""
    ciphertext = []
    kG = scalar_mult(k, G)
    kP = scalar_mult(k, public_key)
    for M in points:
        encrypted_point = point_add(M, kP) if kP != 'O' else M
        ciphertext.append(encrypted_point)
    return (kG, ciphertext)

def ecc_decrypt(kG, encrypted_points, private_key):
    """Decrypts ciphertext using ECC."""
    kP = scalar_mult(private_key, kG)
    plaintext_points = []
    for point in encrypted_points:
        minus_kP = (kP[0], (-kP[1]) % p) if kP != 'O' else 'O'
        decrypted_point = point_add(point, minus_kP) if kP != 'O' else point
        plaintext_points.append(decrypted_point)
    return plaintext_points

def parse_points(input_str):
    """Parses points like (2,7),(5,9) into list of tuples."""
    points = []
    input_str = input_str.strip().replace('),', ')|')
    for pair in input_str.split('|'):
        pair = pair.replace('(', '').replace(')', '').strip()
        if not pair:
            continue
        x, y = pair.split(',')
        points.append((int(x.strip()), int(y.strip())))
    return points

def main():
    G = (2, 7)  # Generator
    private_key = 3
    public_key = scalar_mult(private_key, G)

    print("Elliptic Curve: y^2 = x^3 + x + 6 mod 11")
    print(f"Generator Point G: {G}")
    print(f"Private Key: {private_key}")
    print(f"Public Key: {public_key}")

    print("\nChoose an option:")
    print("E/e: Encryption")
    print("D/d: Decryption")
    choice = input("Enter your choice: ").strip().lower()

    if choice == 'e':
        point_str = input("\nEnter points to encrypt as (x,y),(x,y): ")
        points = parse_points(point_str)
        print("\nPlaintext Points:")
        for pt in points:
            print(pt)

        k = 5  # Fixed random scalar for demo; use random in real apps
        kG, cipher_points = ecc_encrypt(points, public_key, G, k)

        print("\nEncryption Result:")
        print("kG =", kG)
        print("Ciphertext Points:")
        for pt in cipher_points:
            print(pt)

    elif choice == 'd':
        kG_input = input("\nEnter kG as (x,y): ").strip().replace('(', '').replace(')', '')
        kG = tuple(map(int, kG_input.split(',')))

        ciph_str = input("Enter ciphertext points as (x,y),(x,y): ")
        cipher_points = parse_points(ciph_str)

        print("\nCiphertext Points:")
        for pt in cipher_points:
            print(pt)

        decrypted_points = ecc_decrypt(kG, cipher_points, private_key)
        print("\nDecrypted Plaintext Points:")
        for pt in decrypted_points:
            print(pt)

    else:
        print("Invalid choice. Please select E/e or D/d.")

if __name__ == "__main__":
    main()
