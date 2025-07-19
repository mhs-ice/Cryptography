import random

def power_mod(base, exponent, mod):
    """Efficient modular exponentiation"""
    result = 1
    base = base % mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent = exponent >> 1
        base = (base * base) % mod
    return result

def diffie_hellman(p, g, private_a, private_b):
    # Compute public values
    public_a = power_mod(g, private_a, p)
    public_b = power_mod(g, private_b, p)

    # Compute shared secret
    shared_secret_a = power_mod(public_b, private_a, p)
    shared_secret_b = power_mod(public_a, private_b, p)

    return public_a, public_b, shared_secret_a, shared_secret_b

# Example usage
if __name__ == "_main_":
    # Prime modulus and primitive root
    p = int(input("Enter a prime number (p): "))
    g = int(input("Enter a primitive root modulo p (g): "))

    # Private keys (randomly chosen)
    private_a = random.randint(2, p - 2)
    private_b = random.randint(2, p - 2)

    print(f"Alice's Private Key: {private_a}")
    print(f"Bob's Private Key: {private_b}")

    public_a, public_b, secret_a, secret_b = diffie_hellman(p, g, private_a, private_b)

    print(f"Alice's Public Key: {public_a}")
    print(f"Bob's Public Key: {public_b}")
    print(f"Alice's Shared Secret: {secret_a}")
    print(f"Bob's Shared Secret: {secret_b}")

    if secret_a == secret_b:
        print("✅ Shared secret successfully established.")
    else:
        print("❌ Shared secret mismatch.")