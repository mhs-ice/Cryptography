def power_mod(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def is_primitive_root(g, p):
    required_set = set()
    for i in range(1, p):
        mod_result = power_mod(g, i, p)
        if mod_result in required_set:
            return False
        required_set.add(mod_result)
    return True

def find_primitive_root(p):
    """Find the smallest primitive root of prime p."""
    for g in range(2, p):
        if is_primitive_root(g, p):
            return g
    return None

def diffie_hellman_interactive():
    print("\n==== Diffie–Hellman Key Exchange ====\n")

    # Step 1: Get prime number q from user
    q = int(input("Enter a prime number (q): "))

    # Step 2: Find and select a primitive root of q
    g = find_primitive_root(q)
    if g is None:
        print("No primitive root found. Ensure q is prime.")
        return
    print(f"Primitive root (g) of {q} is: {g}")

    # Step 3: Get private keys from user (Xa, Xb < q)
    Xa = int(input("Enter Alice's private key (Xa < q): "))
    Xb = int(input("Enter Bob's private key (Xb < q): "))

    if Xa >= q or Xb >= q:
        print("Error: Private keys must be less than q.")
        return

    # Step 4: Compute public keys
    Ya = power_mod(g, Xa, q)
    Yb = power_mod(g, Xb, q)
    print(f"\nAlice's Public Key : {Ya}")
    print(f"Bob's Public Key : {Yb}")

    # Step 5: Compute shared secret keys
    Ka = power_mod(Yb, Xa, q)
    Kb = power_mod(Ya, Xb, q)

    # Step 6: Compare and print results
    print(f"\nAlice's Shared Secret : {Ka}")
    print(f"Bob's Shared Secret : {Kb}")

    if Ka == Kb:
        print("\n✅ Shared secret successfully established!")
        print(f"Shared Secret Key: {Ka}")
    else:
        print("\n❌ Shared secrets do not match.")

if __name__ == "__main__":
    diffie_hellman_interactive()
