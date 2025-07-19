def main():
    print("Elliptic Curve Cryptography Implementation")
    print("========================================\n")
    
    p = int(input("Enter the value of p of Ep(a,b): "))
    a = int(input("Enter the value of a of Ep(a,b): "))
    b = int(input("Enter the value of b of Ep(a,b): "))
    g_input = input("Enter the generator point G (format: x,y): ")
    g = tuple(map(int, g_input.split(',')))
    
    print(f"\nThe elliptic curve equation is: y² = x³ + {a}x + {b} mod {p}")
    print(f"Generator point G = {g}\n")

    # ========== Key Exchange ==========
    print("Key Exchange Phase:")
    print("------------------")
    
    # Alice's key generation
    alpha = int(input("\nEnter Alice's private key α (1 ≤ α ≤ n-1): "))
    pa = point_multiply(alpha, g, a, p)
    print(f"Alice's public key P_A = αG = {pa}")

    # Bob's key generation
    beta = int(input("Enter Bob's private key β (1 ≤ β ≤ n-1): "))
    pb = point_multiply(beta, g, a, p)
    print(f"Bob's public key P_B = βG = {pb}\n")

    # Shared key computation
    alice_shared_key = point_multiply(alpha, pb, a, p)
    bob_shared_key = point_multiply(beta, pa, a, p)
    
    print(f"Alice computes shared key: αP_B = {alice_shared_key}")
    print(f"Bob computes shared key: βP_A = {bob_shared_key}")
    print("Key exchange successful!" if alice_shared_key == bob_shared_key else "Key exchange failed!")
    
    # ========== Encryption/Decryption ==========
    print("\nEncryption/Decryption Phase:")
    print("---------------------------")
    
    # Message to encrypt
    pm = get_valid_point(p, a, b, "\nEnter message point P_m to encrypt (format: x,y): ")
    
    # Alice's encryption
    alpha_enc = int(input("Enter Alice's random integer α for encryption: "))
    c1 = point_multiply(alpha_enc, g, a, p)
    alpha_pb = point_multiply(alpha_enc, pb, a, p)
    c2 = point_add(pm, alpha_pb, a, p)
    ciphertext = (c1, c2)
    
    print(f"\nEncrypted ciphertext C_m = {ciphertext}")

    # Bob's decryption
    c1, c2 = ciphertext
    beta_c1 = point_multiply(beta, c1, a, p)
    beta_c1_inv = (beta_c1[0], (-beta_c1[1]) % p)  # Negative of the point
    decrypted = point_add(c2, beta_c1_inv, a, p)
    
    print(f"\nDecrypted message = {decrypted}")
    print(f"Original message was {pm}")
    print("Decryption successful!" if decrypted == pm else "Decryption failed!")

def point_add(p, q, a, p_prime):
    """Add two points on the elliptic curve"""
    if p == (0, 0):
        return q
    if q == (0, 0):
        return p
    if p[0] == q[0] and p[1] != q[1]:
        return (0, 0)  # point at infinity
    
    if p != q:
        # Point addition
        m = (q[1] - p[1]) * pow(q[0] - p[0], -1, p_prime)
    else:
        # Point doubling
        m = (3 * p[0]*p[0] + a) * pow(2 * p[1], -1, p_prime)
    
    x_r = (m*m - p[0] - q[0]) % p_prime
    y_r = (m*(p[0] - x_r) - p[1]) % p_prime
    
    return (x_r, y_r)

def point_multiply(k, point, a, p_prime):
    """Multiply point by scalar k using double-and-add algorithm"""
    result = (0, 0)  # point at infinity
    addend = point
    
    while k > 0:
        if k & 1:
            result = point_add(result, addend, a, p_prime)
        addend = point_add(addend, addend, a, p_prime)
        k >>= 1
    
    return result
def is_point_on_curve(point, a, b, p):
    """Check if a point lies on the elliptic curve y² ≡ x³ + ax + b (mod p)"""
    if point == (0, 0):  # Point at infinity (handled separately)
        return True
    
    x, y = point
    return (y ** 2) % p == (x ** 3 + a * x + b) % p

def get_valid_point(p, a, b, prompt="Enter point (format: x,y): "):
    """Get and validate a point on the curve"""
    while True:
        try:
            point_input = input(prompt)
            x, y = map(int, point_input.split(','))
            
            # Check if point is on the curve
            if is_point_on_curve((x, y), a, b, p):
                return (x, y)
            else:
                print(f"Error: Point ({x}, {y}) is not on the curve")
        except ValueError:
            print("Please enter coordinates in format 'x,y'")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()