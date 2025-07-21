# Elliptic Curve Cryptography (ECC) Implementation

def inverse_mod(k, p):
    """Compute the modular inverse of k mod p."""
    if k == 0:
        raise ZeroDivisionError('division by zero')
    return pow(k, p - 2, p)

def is_on_curve(point, a, b, p):
    """Check if the point is on the curve."""
    if point is None:
        return True
    x, y = point
    return (y * y - (x * x * x + a * x + b)) % p == 0

def point_add(point1, point2, a, p):
    """Add two points on the elliptic curve."""
    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        # Point doubling
        m = (3 * x1 * x1 + a) * inverse_mod(2 * y1, p)
    else:
        # Point addition
        m = (y2 - y1) * inverse_mod(x2 - x1, p)

    m = m % p
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

def scalar_mult(k, point, a, p):
    """Multiply a point by an integer k."""
    result = None
    addend = point

    while k:
        if k & 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1

    return result

# Input parameters
p = int(input("Enter prime p: "))           # e.g., 17
a = int(input("Enter curve parameter a: ")) # e.g., 2
b = int(input("Enter curve parameter b: ")) # e.g., 2
Gx = int(input("Enter Gx: "))               # e.g., 5
Gy = int(input("Enter Gy: "))               # e.g., 1
G = (Gx, Gy)
n = int(input("Enter order n: "))           # e.g., 19

print("\nKey Exchange Example:")
alpha = int(input("Enter Alice's private key alpha: ")) # e.g., 3
beta = int(input("Enter Bob's private key beta: "))     # e.g., 9

# Public keys
PA = scalar_mult(alpha, G, a, p)
PB = scalar_mult(beta, G, a, p)
print(f"Alice's public key PA = {PA}")
print(f"Bob's public key PB = {PB}")

# Shared secret
KA = scalar_mult(alpha, PB, a, p)
KB = scalar_mult(beta, PA, a, p)
print(f"Alice computes shared key: {KA}")
print(f"Bob computes shared key:   {KB}")

print("\nEncryption/Decryption Example:")
Pm_x = int(input("Enter message point x: ")) # e.g., 6
Pm_y = int(input("Enter message point y: ")) # e.g., 3
Pm = (Pm_x, Pm_y)

alpha_enc = int(input("Enter sender's private key alpha (for encryption): ")) # e.g., 2
beta_enc = int(input("Enter receiver's private key beta (for encryption): ")) # e.g., 3

PB_enc = scalar_mult(beta_enc, G, a, p)
alphaG = scalar_mult(alpha_enc, G, a, p)
alphaPB = scalar_mult(alpha_enc, PB_enc, a, p)

# Ciphertext
C1 = alphaG
C2 = point_add(Pm, alphaPB, a, p)
print(f"Ciphertext Cm = {{{C1}, {C2}}}")

# Decryption
betaC1 = scalar_mult(beta_enc, C1, a, p)
# Inverse of betaC1
inv_betaC1 = (betaC1[0], (-betaC1[1]) % p)
Pm_decrypted = point_add(C2, inv_betaC1, a, p)
print(f"Decrypted message point: {Pm_decrypted}")

if Pm_decrypted == Pm:
    print("Decryption successful! Message matches original.")
else:
    print("Decryption failed.")