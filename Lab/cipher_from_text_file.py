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
    for key in range(1,95):
        decrypted=encrypt(text,key,'d')
        print(f"Key {key} : {decrypted}")



def main():
    # file=open("myfile.txt","w")
    # file.write("Information and communication engineering\nDept. of ICE\nUniversity of Rajshahi")
    file=open("myfile.txt","r")
    # txt=file.readline()
    # with open("myfile.txt","r") as file:
    mode=input("Enter the mode Encrypt(e) or Decrypt(d) or Brute Force(b):").lower()
    if mode=="b":
        for line in file:
            brute_force(line)
    else:
        key=int(input("Enter key : "))
        for line in file:
            result=encrypt(line,key,mode)
            print(result)
main()
