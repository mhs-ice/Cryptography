def caesar_encrypt(plaintext, shift):
    """
    Encrypts plaintext using Caesar Cipher with the given shift.
    """
    ciphertext = ""
    for char in plaintext:
        if char.isupper():
            ciphertext += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            ciphertext += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            ciphertext += char
    return ciphertext

def caesar_decrypt(ciphertext, shift):
    """
    Decrypts ciphertext using Caesar Cipher with the given shift.
    """
    return caesar_encrypt(ciphertext, -shift)

def brute_force_caesar(ciphertext):
    """
    Performs brute-force attack on Caesar Cipher by trying all possible shifts.
    """
    print("Brute-force attack results:")
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        print(f"Shift {shift:2}: {decrypted}")

def main():
    while True:
        print("\nCaesar Cipher Program")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Brute-Force Attack")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            plaintext = input("Enter plaintext: ")
            shift = int(input("Enter shift value (0-25): "))
            encrypted = caesar_encrypt(plaintext, shift)
            print(f"Encrypted text: {encrypted}")
            
        elif choice == '2':
            ciphertext = input("Enter ciphertext: ")
            shift = int(input("Enter shift value (0-25): "))
            decrypted = caesar_decrypt(ciphertext, shift)
            print(f"Decrypted text: {decrypted}")
            
        elif choice == '3':
            ciphertext = input("Enter ciphertext to brute-force: ")
            brute_force_caesar(ciphertext)
            
        elif choice == '4':
            print("Exiting program...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()