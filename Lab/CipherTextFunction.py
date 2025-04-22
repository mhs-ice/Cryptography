def encrypt(text,key,mode):
    cipher=''
    if mode=='d':
        key=-key
    
    for char in text:
        if 32<=ord(char)<=126:
            # offset = ord("A") if char.isupper() else ord('a')
            shifted = ((ord(char)-32) + key)%95 + 32
            cipher += chr(shifted)
        else:
            cipher+=char
    return cipher
def brute_force(text):
    print("Trying all possible keys...")
    for key in range(1,26):
        decrypted=encrypt(text,key,'d')
        print(f"Key {key} : {decrypted}")


def main():
    plainText=input("Enter your text : ")
    key=int(input("Enter key : "))
    mode=input("Enter the mode Encrypt(e) or Decrypt(d) Brute Force(b):").lower()
    if mode=='b':
        brute_force(plainText)
    
    else:
        result=encrypt(plainText,key,mode)
        print(result)
main()


    