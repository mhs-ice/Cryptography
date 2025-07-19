import random

# ---------- Extended Euclidean Algorithm ----------
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# ---------- Modular Inverse ----------
def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise Exception("Modular inverse doesn't exist.")
    else:
        return x % phi

# ---------- Check for Primality (simple) ----------
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

# ---------- Generate Public and Private Keys ----------
def generate_keys():
    # Choose two distinct prime numbers p and q
    while True:
        p = random.randint(50, 100)
        q = random.randint(50, 100)
        if is_prime(p) and is_prime(q) and p != q:
            break

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose public exponent e such that 1 < e < phi and gcd(e, phi) = 1
    e = 3
    while True:
        if extended_gcd(e, phi)[0] == 1:
            break
        e += 2

    # Compute private key d
    d = mod_inverse(e, phi)

    return (e, n), (d, n)

# ---------- Encryption ----------
def encrypt(message, public_key):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher

# ---------- Decryption ----------
def decrypt(cipher, private_key):
    d, n = private_key
    decrypted = ''.join([chr(pow(char, d, n)) for char in cipher])
    return decrypted

# ---------- File Operations ----------
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(str(content))

# ---------- Main Function ----------
if __name__ == "__main__":
    public_key, private_key = generate_keys()

    print(f"Public Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")

    # Read plaintext from file
    input_file = "plaintext.txt"
    message = read_file(input_file)
    print(f"Original message from file: {message}")

    # Encrypt and save to file
    cipher = encrypt(message, public_key)
    write_file("encrypted.txt", cipher)
    print("Encrypted message saved to encrypted.txt")

    # Decrypt and save to file
    decrypted_message = decrypt(cipher, private_key)
    write_file("decrypted.txt", decrypted_message)
    print("Decrypted message saved to decrypted.txt")

    # Print results
    print(f"Encrypted data: {cipher}")
    print(f"Decrypted message: {decrypted_message}")