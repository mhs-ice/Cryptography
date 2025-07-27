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

def cbc_encrypt(message, key, iv, block_size):
    binary_data = text_to_binary(message)
    original_len = len(binary_data)
    padded = pad_binary(binary_data, block_size)
    blocks = split_into_blocks(padded, block_size)
    ciphertext = []
    prev = iv
    for block in blocks:
        xored = xor_bits(block, prev)
        encrypted = xor_bits(xored, key)
        ciphertext.append(encrypted)
        prev = encrypted
    return ''.join(ciphertext), original_len

def cbc_decrypt(cipher_binary, key, iv, block_size, original_len):
    blocks = split_into_blocks(cipher_binary, block_size)
    plaintext = []
    prev = iv
    for block in blocks:
        decrypted = xor_bits(block, key)
        original = xor_bits(decrypted, prev)
        plaintext.append(original)
        prev = block
    binary = ''.join(plaintext)
    return binary_to_text(binary[:original_len])

if __name__ == "__main__":
    message = "Information and Communication Engineering"
    block_size = 10
    key = '1010101010'
    iv = '1110001110'

    print("Original Message:", message)
    cipher, length = cbc_encrypt(message, key, iv, block_size)
    print("Encrypted Text:", binary_to_text(pad_binary(cipher, 8)))
    print("Decrypted Text:", cbc_decrypt(cipher, key, iv, block_size, length))
