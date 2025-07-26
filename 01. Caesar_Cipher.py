def caesar_encrypt(plaintext,shift):
    ciphertext=""
    for char in plaintext:
        if char.isupper():
            ciphertext+=chr((ord(char)+shift-65)%26+65)

        elif char.islower():
            ciphertext+=chr((ord(char)+shift-97)%26+97)
        # base= ord('a') if char.islower() else ord('A')
        # if char.isalpha():
        #     ciphertext+=chr((ord(char.lower())+shift-97)%26+97)
        # if char.isalpha():
        #     ciphertext+=chr((ord(char.upper())+shift-65)%26+65)

        elif char.isdigit():
            ciphertext+=chr((ord(char)+shift-48)%10+48)

        else:
            ciphertext+=char
    
    return ciphertext
    
def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

def brute_force_caesar(ciphertext):
    for shift in range(26):
        decrypted= caesar_decrypt(ciphertext, shift)
        print(f"Shift {shift}: {decrypted}")
    

def main():
    while(True):
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Brute Force")
        print("4. Exit")

        choice = input("Enter ur choicce:")
        if choice=='1':
            plaintext=input("Enter the plaintext:")
            shift=int(input("Enter the shift value:"))
            encrypted= caesar_encrypt(plaintext,shift)
            print("Encrypted text :", encrypted)

        elif choice=='2':
            ciphertext=input("Enter the ciphertext:")
            shift=int(input("Enter the shift value:"))
            decrypted=caesar_decrypt(ciphertext, shift)
            print("Decrypted text :", decrypted)
        
        elif choice=='3':
            ciphertext=input("Enter ciphertext to brute force attack:")
            brute_force_caesar(ciphertext)

        elif choice=='4':
            print("Exiting ....")
            break

        else:
            print("Invalid choice")

if __name__=="__main__":
    main()