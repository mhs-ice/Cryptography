def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def multiplicative_inverse(e, phi):
    d_old, d = 0, 1
    r_old, r = phi, e
    while r != 0:
        quotient = r_old // r
        d_old, d = d, d_old - quotient * d
        r_old, r = r, r_old - quotient * r
    return d_old % phi

def number_to_text(num_str):
    # প্রতি ২ ডিজিট = ১ অক্ষর বা স্পেস
    text = ''
    for i in range(0, len(num_str), 2):
        part = num_str[i:i+2]
        num = int(part)
        if 1 <= num <= 26:
            text += chr(num + 64)  # A = 65
        elif num == 27:
            text += ' '
        else:
            text += '?'
    return text

def text_to_number(text):
    # A-Z = 01-26, SPACE = 27
    result = ''
    for c in text.upper():
        if c == ' ':
            result += '27'
        elif 'A' <= c <= 'Z':
            result += str(ord(c)-64).zfill(2)
        else:
            result += '00'  # invalid char fallback
    return result

def main():
    print("🔐 RSA Custom System with A-Z and SPACE\n")

    # Step 1: Input two primes
    p = int(input("Enter first prime (p): "))
    q = int(input("Enter second prime (q): "))
    if not (is_prime(p) and is_prime(q)):
        print("❌ Both numbers must be prime.")
        return
    n = p * q
    phi = (p - 1) * (q - 1)

    # Step 2: Input public key (e, n)
    e = int(input("Enter public key e: "))
    user_n = int(input("Enter public key n: "))
    if user_n != n:
        print(f"⚠️ Warning: You provided n={user_n}, but correct n should be {n}. Proceeding anyway...")

    # Step 3: Input encrypted number (like 4020)
    encrypted_number = int(input("Enter encrypted number: "))

    # Step 4: Generate private key (d, n)
    d = multiplicative_inverse(e, phi)
    print(f"\n🔑 Generated Private Key: d = {d}, n = {n}")

    # Step 5: Decrypt the number
    decrypted_number = pow(encrypted_number, d, n)
    decrypted_str = str(decrypted_number).zfill(4)  # Ensure it's at least 4 digits
    print(f"🔓 Decrypted numeric form: {decrypted_str}")

    # Step 6: Convert number to text (A-Z + SPACE)
    message = number_to_text(decrypted_str)
    print(f"📩 Decrypted message: {message}")

    # Step 7: Encrypt again using public key
    re_encrypted_number = pow(decrypted_number, e, n)
    print(f"🔐 Re-encrypted number using public key: {re_encrypted_number}")

if __name__ == "__main__":
    main()
