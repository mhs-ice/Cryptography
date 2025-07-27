def caesar_cipher(text, shift):
    result = ''
    for char in text:
        if char.isupper():
            shifted = ((ord(char) - ord('A') + shift) % 26) + ord('A')
            result += chr(shifted)
        elif char.islower():
            shifted = ((ord(char) - ord('a') + shift) % 26) + ord('a')
            result += chr(shifted)
        else:
            result += char
    return result

def main():
    print("===== Caesar Cipher (Letters only) =====")
    print("Choose an option:")
    print("E/e: Encryption")
    print("D/d: Decryption")
    choice = input("Enter your choice: ").strip().lower()

    if choice not in ['e', 'd']:
        print("Invalid choice! Please enter E or D.")
        return

    text = input("Enter your message: ")
    try:
        shift = int(input("Enter shift value : "))
    except ValueError:
        print("Shift must be an integer!")
        return

    if choice == 'd':
        shift = -shift  # Reverse shift for decryption

    result = caesar_cipher(text, shift)

    print("\nOriginal Message:", text)
    print("Shift Applied:", shift)
    print("Resulting Message:", result)

if __name__ == "__main__":
    main()
