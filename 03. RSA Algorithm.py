import random
import math
from math import gcd

def is_prime(n, k=5):
    """Miller-Rabin primality test"""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False
    
    # Write n as d*2^s + 1
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a large prime number"""
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1  # Set MSB and LSB to ensure size and oddness
        if is_prime(p):
            return p

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Modular inverse using Extended Euclidean Algorithm"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def generate_keys(bits=64):
    """Generate RSA public and private keys"""
    # Choose two large primes
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    
    # Ensure p and q are different
    while p == q:
        q = generate_prime(bits // 2)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    # Compute d, the modular inverse of e
    d = modinv(e, phi)
    
    # Public key: (e, n), Private key: (d, n)
    return ((e, n), (d, n))

def encrypt(message, public_key):
    """Encrypt message using public key"""
    e, n = public_key
    # Convert each character to ASCII and encrypt
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted

def decrypt(encrypted, private_key):
    """Decrypt message using private key"""
    d, n = private_key
    # Decrypt each number to character
    decrypted = [chr(pow(num, d, n)) for num in encrypted]
    return ''.join(decrypted)

# Example usage
if __name__ == "__main__":
    # Generate keys (small bits for demo, use >=1024 in practice)
    public_key, private_key = generate_keys(32)
    print("Public Key (e, n):", public_key)
    print("Private Key (d, n):", private_key)
    
    # Encrypt a message
    # message = "Hello RSA!"
    message = input("Enter the message : ")
    print("\nOriginal Message:", message)
    
    encrypted = encrypt(message, public_key)
    print("Encrypted Message:", encrypted)
    
    # Decrypt the message
    decrypted = decrypt(encrypted, private_key)
    print("Decrypted Message:", decrypted)