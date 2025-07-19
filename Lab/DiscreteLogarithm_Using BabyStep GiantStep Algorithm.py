from math import gcd, sqrt, ceil
from collections import defaultdict

def baby_step_giant_step(g, h, p):
    """Solves g^x ≡ h (mod p) using Baby-step Giant-step."""
    n = ceil(sqrt(p - 1))
    
    # Baby-step: Store g^j mod p in a dictionary
    table = defaultdict(int)
    curr = 1
    for j in range(n + 1):
        table[curr] = j
        curr = (curr * g) % p
    
    # Giant-step: Compute h * g^{-in} mod p and check
    g_inv = pow(g, n * (p - 2), p)  # Fermat's little theorem for inverse
    curr = h
    for i in range(n + 1):
        if curr in table:
            return i * n + table[curr]
        curr = (curr * g_inv) % p
    
    return None  # No solution exists

# Example: Find x such that 3^x ≡ 13 mod 17
# g, h, p = 3, 13, 17
g=int(input("Enter base (g) :"))
h=int(input("Enter remainder (h) :"))
p=int(input("Enter modulus (p) :"))
x = baby_step_giant_step(g, h, p)
print(f"Solution: x = {x}")  # Output: 4 (since 3^4 ≡ 13 mod 17)