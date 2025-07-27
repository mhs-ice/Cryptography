import string

# Define all characters to shift
ALL_CHARS = string.ascii_letters + string.digits + string.punctuation + ' '

def caesar_cipher(text, shift):
    result = ''
    for char in text:
        if char in ALL_CHARS:
            idx = ALL_CHARS.index(char)
            new_idx = (idx + shift) % len(ALL_CHARS)
            result += ALL_CHARS[new_idx]
        else:
            result += char  # Keep unexpected characters as-is
    return result

def main():
    print("===== Caesar Cipher (Handles Letters, Digits, Punctuation, Space) =====")
    print("Choose an option:")
    print("E/e: Encryption")
    print("D/d: Decryption")
    choice = input("Enter your choice: ").strip().lower()

    if choice not in ['e', 'd']:
        print("Invalid choice! Please enter E or D.")
        return

    text = input("Enter your message: ")
    try:
        shift = int(input("Enter shift value (e.g., 3 or -3): "))
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
