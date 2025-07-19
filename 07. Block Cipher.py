import os

BLOCK_SIZE = 8  # 8 bytes (64 bits)
KEY = b'\x13\x57\x9B\xDF\x02\x46\x8A\xCE'  # example 64-bit key

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pad(data):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# Toy block cipher: XOR with fixed key
def encrypt_block(block):
    return xor_bytes(block, KEY)

def decrypt_block(block):
    return xor_bytes(block, KEY)

# ECB Mode
def ecb_encrypt(plaintext):
    plaintext = pad(plaintext)
    blocks = [plaintext[i:i+BLOCK_SIZE] for i in range(0, len(plaintext), BLOCK_SIZE)]
    ciphertext = b''.join(encrypt_block(block) for block in blocks)
    return ciphertext

def ecb_decrypt(ciphertext):
    blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    plaintext = b''.join(decrypt_block(block) for block in blocks)
    return unpad(plaintext)

# CBC Mode
def cbc_encrypt(plaintext, iv):
    plaintext = pad(plaintext)
    blocks = [plaintext[i:i+BLOCK_SIZE] for i in range(0, len(plaintext), BLOCK_SIZE)]
    ciphertext = b''
    prev = iv
    for block in blocks:
        xor_block = xor_bytes(block, prev)
        enc_block = encrypt_block(xor_block)
        ciphertext += enc_block
        prev = enc_block
    return ciphertext

def cbc_decrypt(ciphertext, iv):
    blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    plaintext = b''
    prev = iv
    for block in blocks:
        dec_block = decrypt_block(block)
        plain_block = xor_bytes(dec_block, prev)
        plaintext += plain_block
        prev = block
    return unpad(plaintext)

# CFB Mode
def cfb_encrypt(plaintext, iv):
    plaintext = pad(plaintext)
    ciphertext = b''
    prev = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        keystream = encrypt_block(prev)
        block = plaintext[i:i+BLOCK_SIZE]
        cipher_block = xor_bytes(block, keystream)
        ciphertext += cipher_block
        prev = cipher_block
    return ciphertext

def cfb_decrypt(ciphertext, iv):
    plaintext = b''
    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        keystream = encrypt_block(prev)
        block = ciphertext[i:i+BLOCK_SIZE]
        plain_block = xor_bytes(block, keystream)
        plaintext += plain_block
        prev = block
    return unpad(plaintext)

# OFB Mode
def ofb_encrypt_decrypt(data, iv):
    result = b''
    prev = iv
    for i in range(0, len(data), BLOCK_SIZE):
        keystream = encrypt_block(prev)
        block = data[i:i+BLOCK_SIZE]
        output_block = xor_bytes(block, keystream[:len(block)])
        result += output_block
        prev = keystream
    return result

# Main function to test
def main():
    message = b"This is a test message for block cipher modes."
    iv = os.urandom(BLOCK_SIZE)

    print("\n--- ECB ---")
    ctext = ecb_encrypt(message)
    print("Ciphertext:", ctext.hex())
    print("Decrypted :", ecb_decrypt(ctext))

    print("\n--- CBC ---")
    ctext = cbc_encrypt(message, iv)
    print("Ciphertext:", ctext.hex())
    print("Decrypted :", cbc_decrypt(ctext, iv))

    print("\n--- CFB ---")
    ctext = cfb_encrypt(message, iv)
    print("Ciphertext:", ctext.hex())
    print("Decrypted :", cfb_decrypt(ctext, iv))

    print("\n--- OFB ---")
    padded_message = pad(message)
    ctext = ofb_encrypt_decrypt(padded_message, iv)
    print("Ciphertext:", ctext.hex())
    ptext = ofb_encrypt_decrypt(ctext, iv)
    print("Decrypted :", unpad(ptext))

if __name__ == "__main__":
    main()
