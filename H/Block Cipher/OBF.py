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

def ofb_encrypt(message, key, iv, block_size):
    binary_data = text_to_binary(message)
    original_len = len(binary_data)
    padded = pad_binary(binary_data, block_size)
    blocks = split_into_blocks(padded, block_size)
    ciphertext = []
    feedback = iv
    for block in blocks:
        output = xor_bits(feedback, key)
        cipher_block = xor_bits(block, output)
        ciphertext.append(cipher_block)
        feedback = output
    return ''.join(ciphertext), original_len

def ofb_decrypt(cipher_binary, key, iv, block_size, original_len):
    blocks = split_into_blocks(cipher_binary, block_size)
    plaintext = []
    feedback = iv
    for block in blocks:
        output = xor_bits(feedback, key)
        plain_block = xor_bits(block, output)
        plaintext.append(plain_block)
        feedback = output
    binary = ''.join(plaintext)
    return binary_to_text(binary[:original_len])

if __name__ == "__main__":
    message = "Information and Communication Engineering"
    block_size = 10
    key = '1010101010'
    iv = '1110001110'

    print("Original Message:", message)
    cipher, length = ofb_encrypt(message, key, iv, block_size)
    print("Encrypted Text:", binary_to_text(pad_binary(cipher, 8)))
    print("Decrypted Text:", ofb_decrypt(cipher, key, iv, block_size, length))
