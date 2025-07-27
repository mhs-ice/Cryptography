def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(c, 2)) for c in chars])

def pad_binary(binary, block_size):
    padding_len = (block_size - len(binary) % block_size) % block_size
    return binary + '0' * padding_len

def xor_bits(a, b):
    return ''.join(['1' if x != y else '0' for x, y in zip(a, b)])

def split_into_blocks(binary, block_size):
    return [binary[i:i+block_size] for i in range(0, len(binary), block_size)]

# ECB Mode
def ecb_encrypt(binary, key, block_size):
    blocks = split_into_blocks(binary, block_size)
    encrypted_blocks = [xor_bits(block, key) for block in blocks]
    return ''.join(encrypted_blocks)

def ecb_decrypt(cipher_binary, key, block_size):
    return ecb_encrypt(cipher_binary, key, block_size)

# CBC Mode
def cbc_encrypt(binary, key, iv, block_size):
    blocks = split_into_blocks(binary, block_size)
    ciphertext_blocks = []
    prev = iv
    for block in blocks:
        xored = xor_bits(block, prev)
        encrypted = xor_bits(xored, key)
        ciphertext_blocks.append(encrypted)
        prev = encrypted
    return ''.join(ciphertext_blocks)

def cbc_decrypt(cipher_binary, key, iv, block_size):
    blocks = split_into_blocks(cipher_binary, block_size)
    plaintext_blocks = []
    prev = iv
    for block in blocks:
        decrypted = xor_bits(block, key)
        original = xor_bits(decrypted, prev)
        plaintext_blocks.append(original)
        prev = block
    return ''.join(plaintext_blocks)

# Convert encrypted binary to Cipher Text
def binary_to_cipher_text(binary):
    padded = pad_binary(binary, 8)
    return binary_to_text(padded)

def cipher_text_to_binary(cipher_text):
    return text_to_binary(cipher_text)

# Main Code
if __name__ == "__main__":
    message ="Information and Communication Enginering"
    block_size = 10
    key = '1010101010'
    iv = '1110001110'

    print("Original Message:", message)

    # Convert message to binary
    binary_data = text_to_binary(message)
    padded_binary = pad_binary(binary_data, block_size)

    # ECB Mode 
    ecb_encrypted_binary = ecb_encrypt(padded_binary, key, block_size)
    ecb_cipher_text = binary_to_cipher_text(ecb_encrypted_binary)
    print("\nECB Encrypted Text:", ecb_cipher_text)

    # Decryption
    ecb_cipher_binary_back = cipher_text_to_binary(ecb_cipher_text)
    ecb_decrypted_binary = ecb_decrypt(ecb_cipher_binary_back, key, block_size)
    ecb_decrypted_message = binary_to_text(ecb_decrypted_binary)
    print("ECB Decrypted Message:", ecb_decrypted_message)

    # CBC Mode 
    cbc_encrypted_binary = cbc_encrypt(padded_binary, key, iv, block_size)
    cbc_cipher_text = binary_to_cipher_text(cbc_encrypted_binary)
    print("\nCBC Encrypted Text:", cbc_cipher_text)

    # Decryption
    cbc_cipher_binary_back = cipher_text_to_binary(cbc_cipher_text)
    cbc_decrypted_binary = cbc_decrypt(cbc_cipher_binary_back, key, iv, block_size)
    cbc_decrypted_message = binary_to_text(cbc_decrypted_binary)
    print("CBC Decrypted Message:", cbc_decrypted_message)
