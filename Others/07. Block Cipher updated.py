import random

class BlockCipher:
    """Simple block cipher for demonstration purposes"""
    def __init__(self, key, block_size=8):
        self.key = key
        self.block_size = block_size
    
    def encrypt_block(self, block):
        """Simple XOR-based encryption for demonstration"""
        if len(block) != self.block_size:
            raise ValueError(f"Block must be {self.block_size} bytes")
        
        # Simple XOR with key (repeated if necessary)
        encrypted = bytearray()
        for i in range(len(block)):
            encrypted.append(block[i] ^ self.key[i % len(self.key)])
        return bytes(encrypted)
    
    def decrypt_block(self, block):
        """For XOR cipher, decryption is the same as encryption"""
        return self.encrypt_block(block)


class BlockCipherModes:
    def __init__(self, cipher):
        self.cipher = cipher
        self.block_size = cipher.block_size
    
    def pad(self, data):
        """PKCS7 padding"""
        padding_length = self.block_size - (len(data) % self.block_size)
        if padding_length == 0:
            padding_length = self.block_size
        return data + bytes([padding_length] * padding_length)
    
    def unpad(self, data):
        """Remove PKCS7 padding"""
        padding_length = data[-1]
        return data[:-padding_length]
    
    def xor_bytes(self, a, b):
        """XOR two byte sequences"""
        return bytes(x ^ y for x, y in zip(a, b))
    
    # ECB Mode
    def ecb_encrypt(self, plaintext):
        """Electronic Codebook mode encryption"""
        padded = self.pad(plaintext)
        ciphertext = bytearray()
        
        for i in range(0, len(padded), self.block_size):
            block = padded[i:i + self.block_size]
            encrypted_block = self.cipher.encrypt_block(block)
            ciphertext.extend(encrypted_block)
        
        return bytes(ciphertext)
    
    def ecb_decrypt(self, ciphertext):
        """Electronic Codebook mode decryption"""
        plaintext = bytearray()
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = self.cipher.decrypt_block(block)
            plaintext.extend(decrypted_block)
        
        return self.unpad(bytes(plaintext))
    
    # CBC Mode
    def cbc_encrypt(self, plaintext, iv):
        """Cipher Block Chaining mode encryption"""
        if len(iv) != self.block_size:
            raise ValueError(f"IV must be {self.block_size} bytes")
        
        padded = self.pad(plaintext)
        ciphertext = bytearray()
        previous_block = iv
        
        for i in range(0, len(padded), self.block_size):
            block = padded[i:i + self.block_size]
            xored = self.xor_bytes(block, previous_block)
            encrypted_block = self.cipher.encrypt_block(xored)
            ciphertext.extend(encrypted_block)
            previous_block = encrypted_block
        
        return bytes(ciphertext)
    
    def cbc_decrypt(self, ciphertext, iv):
        """Cipher Block Chaining mode decryption"""
        if len(iv) != self.block_size:
            raise ValueError(f"IV must be {self.block_size} bytes")
        
        plaintext = bytearray()
        previous_block = iv
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = self.cipher.decrypt_block(block)
            xored = self.xor_bytes(decrypted_block, previous_block)
            plaintext.extend(xored)
            previous_block = block
        
        return self.unpad(bytes(plaintext))
    
    # CFB Mode
    def cfb_encrypt(self, plaintext, iv):
        """Cipher Feedback mode encryption"""
        if len(iv) != self.block_size:
            raise ValueError(f"IV must be {self.block_size} bytes")
        
        ciphertext = bytearray()
        feedback = iv
        
        for i in range(0, len(plaintext), self.block_size):
            encrypted_feedback = self.cipher.encrypt_block(feedback)
            block = plaintext[i:i + self.block_size]
            
            # Handle last block which might be shorter
            cipher_block = self.xor_bytes(block, encrypted_feedback[:len(block)])
            ciphertext.extend(cipher_block)
            
            # Update feedback
            if len(block) == self.block_size:
                feedback = cipher_block
            else:
                # For partial blocks, shift feedback and append cipher block
                feedback = feedback[len(block):] + cipher_block
        
        return bytes(ciphertext)
    
    def cfb_decrypt(self, ciphertext, iv):
        """Cipher Feedback mode decryption"""
        if len(iv) != self.block_size:
            raise ValueError(f"IV must be {self.block_size} bytes")
        
        plaintext = bytearray()
        feedback = iv
        
        for i in range(0, len(ciphertext), self.block_size):
            encrypted_feedback = self.cipher.encrypt_block(feedback)
            block = ciphertext[i:i + self.block_size]
            
            # Handle last block which might be shorter
            plain_block = self.xor_bytes(block, encrypted_feedback[:len(block)])
            plaintext.extend(plain_block)
            
            # Update feedback
            if len(block) == self.block_size:
                feedback = block
            else:
                # For partial blocks, shift feedback and append cipher block
                feedback = feedback[len(block):] + block
        
        return bytes(plaintext)
    
    # OFB Mode
    def ofb_encrypt(self, plaintext, iv):
        """Output Feedback mode encryption"""
        if len(iv) != self.block_size:
            raise ValueError(f"IV must be {self.block_size} bytes")
        
        ciphertext = bytearray()
        feedback = iv
        
        for i in range(0, len(plaintext), self.block_size):
            feedback = self.cipher.encrypt_block(feedback)
            block = plaintext[i:i + self.block_size]
            
            # Handle last block which might be shorter
            cipher_block = self.xor_bytes(block, feedback[:len(block)])
            ciphertext.extend(cipher_block)
        
        return bytes(ciphertext)
    
    def ofb_decrypt(self, ciphertext, iv):
        """Output Feedback mode decryption (same as encryption for OFB)"""
        return self.ofb_encrypt(ciphertext, iv)


def generate_random_bytes(length):
    """Generate random bytes for keys and IVs"""
    return bytes([random.randint(0, 255) for _ in range(length)])


def demonstrate_modes():
    """Demonstrate all block cipher modes"""
    # Setup
    block_size = 8
    key = generate_random_bytes(block_size)
    iv = generate_random_bytes(block_size)
    
    cipher = BlockCipher(key, block_size)
    modes = BlockCipherModes(cipher)
    
    # Test message
    plaintext = b"Hello, this is a test message for block cipher modes!"
    print(f"Original plaintext: {plaintext}")
    print(f"Plaintext length: {len(plaintext)} bytes")
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print("-" * 60)
    
    # ECB Mode
    print("\n1. ECB (Electronic Codebook) Mode:")
    ecb_encrypted = modes.ecb_encrypt(plaintext)
    ecb_decrypted = modes.ecb_decrypt(ecb_encrypted)
    print(f"Encrypted: {ecb_encrypted.hex()}")
    print(f"Decrypted: {ecb_decrypted}")
    print(f"Match: {plaintext == ecb_decrypted}")
    
    # CBC Mode
    print("\n2. CBC (Cipher Block Chaining) Mode:")
    cbc_encrypted = modes.cbc_encrypt(plaintext, iv)
    cbc_decrypted = modes.cbc_decrypt(cbc_encrypted, iv)
    print(f"Encrypted: {cbc_encrypted.hex()}")
    print(f"Decrypted: {cbc_decrypted}")
    print(f"Match: {plaintext == cbc_decrypted}")
    
    # CFB Mode
    print("\n3. CFB (Cipher Feedback) Mode:")
    cfb_encrypted = modes.cfb_encrypt(plaintext, iv)
    cfb_decrypted = modes.cfb_decrypt(cfb_encrypted, iv)
    print(f"Encrypted: {cfb_encrypted.hex()}")
    print(f"Decrypted: {cfb_decrypted}")
    print(f"Match: {plaintext == cfb_decrypted}")
    
    # OFB Mode
    print("\n4. OFB (Output Feedback) Mode:")
    ofb_encrypted = modes.ofb_encrypt(plaintext, iv)
    ofb_decrypted = modes.ofb_decrypt(ofb_encrypted, iv)
    print(f"Encrypted: {ofb_encrypted.hex()}")
    print(f"Decrypted: {ofb_decrypted}")
    print(f"Match: {plaintext == ofb_decrypted}")
    
    # Demonstrate that ECB produces identical ciphertext for identical blocks
    print("\n" + "-" * 60)
    print("ECB Mode Pattern Demonstration:")
    repeated_plaintext = b"SAME_BLK" * 5  # Repeated 8-byte blocks
    ecb_repeated = modes.ecb_encrypt(repeated_plaintext)
    print(f"Plaintext with repeated blocks: {repeated_plaintext}")
    print(f"ECB encrypted: {ecb_repeated.hex()}")
    print("Notice: Identical plaintext blocks produce identical ciphertext blocks in ECB")
    
    # Compare with CBC
    cbc_repeated = modes.cbc_encrypt(repeated_plaintext, iv)
    print(f"CBC encrypted: {cbc_repeated.hex()}")
    print("Notice: CBC produces different ciphertext for identical plaintext blocks")


if __name__ == "__main__":
    demonstrate_modes()