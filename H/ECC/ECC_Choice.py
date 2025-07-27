# Elliptic Curve Cryptography with manual XOR encryption (no libraries)
# Curve: y^2 = x^3 + 2x + 3 over F_97

def modinv(a, p):
    # Extended Euclidean Algorithm for Modular Inverse
    if a == 0:
        return None
    lm, hm = 1, 0
    low, high = a % p, p
    while low > 1:
        r = high // low
        nm, new = hm - lm * r, high - low * r
        lm, low, hm, high = nm, new, lm, low
    return lm % p

class EllipticCurve:
    def __init__(self, a, b, p, g):
        self.a = a
        self.b = b
        self.p = p
        self.g = g
        self.infinity = (None, None)

    def is_on_curve(self, P):
        if P == self.infinity:
            return True
        x, y = P
        return (y ** 2 - x ** 3 - self.a * x - self.b) % self.p == 0

    def point_add(self, P, Q):
        if P == self.infinity:
            return Q
        if Q == self.infinity:
            return P
        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y1 != y2:
            return self.infinity

        if P == Q:
            return self.point_double(P)

        m = ((y2 - y1) * modinv(x2 - x1, self.p)) % self.p
        x3 = (m * m - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def point_double(self, P):
        if P == self.infinity:
            return P
        x, y = P
        if y == 0:
            return self.infinity
        m = ((3 * x * x + self.a) * modinv(2 * y, self.p)) % self.p
        x3 = (m * m - 2 * x) % self.p
        y3 = (m * (x - x3) - y) % self.p
        return (x3, y3)

    def scalar_mult(self, k, P):
        R = self.infinity
        while k > 0:
            if k & 1:
                R = self.point_add(R, P)
            P = self.point_double(P)
            k >>= 1
        return R

# Simplified key derivation from shared point
def derive_key(point):
    x, y = point
    # Combine x and y into a simple integer hash
    return (x * 100 + y) % 256  # Fit into 1-byte key

# XOR-based symmetric encryption
def xor_encrypt(key, plaintext):
    return bytes([ord(c) ^ key for c in plaintext])

def xor_decrypt(key, ciphertext):
    return ''.join([chr(b ^ key) for b in ciphertext])

# Main Program
def main():
    a, b, p = 2, 3, 97
    G = (3, 6)
    curve = EllipticCurve(a, b, p, G)

    print("Choose an option:")
    print("E/e: Encryption")
    print("D/d: Decryption")
    choice = input("Enter your choice: ").strip().lower()

    if choice == 'e':
        alice_private = int(input("Enter Alice's private key: "))
        bob_private = int(input("Enter Bob's private key: "))
        plaintext = input("Enter the plaintext message: ")

        alice_public = curve.scalar_mult(alice_private, G)
        bob_public = curve.scalar_mult(bob_private, G)

        print(f"\nAlice Public Key: {alice_public}")
        print(f"Bob Public Key:   {bob_public}")

        shared_secret_alice = curve.scalar_mult(alice_private, bob_public)
        shared_secret_bob = curve.scalar_mult(bob_private, alice_public)

        assert shared_secret_alice == shared_secret_bob
        print(f"Shared Secret:    {shared_secret_alice}")

        key = derive_key(shared_secret_alice)

        ciphertext_bytes = xor_encrypt(key, plaintext)
        print("Plaintext Message: ", plaintext)
        print("Encrypted Message (hex):", ciphertext_bytes.hex())

    elif choice == 'd':
        alice_private = int(input("Enter Alice's private key: "))
        bob_private = int(input("Enter Bob's private key: "))
        ciphertext_hex = input("Enter the ciphertext message (hex): ")

        alice_public = curve.scalar_mult(alice_private, G)
        bob_public = curve.scalar_mult(bob_private, G)

        print(f"\nAlice Public Key: {alice_public}")
        print(f"Bob Public Key:   {bob_public}")

        shared_secret_alice = curve.scalar_mult(alice_private, bob_public)
        shared_secret_bob = curve.scalar_mult(bob_private, alice_public)

        assert shared_secret_alice == shared_secret_bob
        print(f"Shared Secret:    {shared_secret_alice}")

        key = derive_key(shared_secret_alice)

        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        decrypted_text = xor_decrypt(key, ciphertext_bytes)
        print("Ciphertext Message (hex):", ciphertext_hex)
        print("Decrypted Message:        ", decrypted_text)

    else:
        print("Invalid choice! Please enter E/e or D/d.")

if __name__ == "__main__":
    main()
