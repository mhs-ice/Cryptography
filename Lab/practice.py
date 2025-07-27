import os

BLOCK_SIZE_BITS = 64  # 64 bits
BLOCK_SIZE_BYTES = BLOCK_SIZE_BITS // 8
KEY = 0x13579BDF02468ACE  # example 64-bit key as integer

def int_to_bits(n, length=64):
    """Convert integer to bit array"""
    return [int(b) for b in format(n, f'0{length}b')]

def bits_to_int(bits):
    """Convert bit array to integer"""
    return int(''.join(map(str, bits)), 2)

def xor_bits(a, b):
    """XOR two bit arrays"""
    return [x ^ y for x, y in zip(a, b)]

def pad_bits(data_bits):
    """Pad bit array to multiple of BLOCK_SIZE_BITS"""
    pad_len = BLOCK_SIZE_BITS - (len(data_bits) % BLOCK_SIZE_BITS)
    return data_bits + [0] * pad_len  # or use PKCS#7-like padding

# Toy block cipher: XOR with fixed key (bit level)
def encrypt_block_bits(block_bits):
    key_bits = int_to_bits(KEY)
    return xor_bits(block_bits, key_bits)

# CBC Mode with bit-level operations
def cbc_encrypt_bits(plaintext_bits, iv_bits):
    plaintext_bits = pad_bits(plaintext_bits)
    blocks = [plaintext_bits[i:i+BLOCK_SIZE_BITS] 
             for i in range(0, len(plaintext_bits), BLOCK_SIZE_BITS)]
    ciphertext_bits = []
    prev = iv_bits
    for block in blocks:
        xor_block = xor_bits(block, prev)
        enc_block = encrypt_block_bits(xor_block)
        ciphertext_bits.extend(enc_block)
        prev = enc_block
    return ciphertext_bits

def main_bits():
    message = "This is a test message for block cipher modes."
    
    # Convert message to bits
    message_bits = []
    for byte in message.encode('utf-8'):
        message_bits.extend(int_to_bits(byte, 8))
    
    # Generate random IV
    iv = os.urandom(BLOCK_SIZE_BYTES)
    iv_bits = []
    for byte in iv:
        iv_bits.extend(int_to_bits(byte, 8))
    
    print("\n--- CBC (Bit Level) ---")
    ctext_bits = cbc_encrypt_bits(message_bits, iv_bits)
    
    # Convert ciphertext bits back to bytes for display
    ctext_bytes = bytes([bits_to_int(ctext_bits[i:i+8]) 
                     for i in range(0, len(ctext_bits), 8)])
    print("Ciphertext:", ctext_bytes.hex())

if __name__ == "__main__":
    main_bits()