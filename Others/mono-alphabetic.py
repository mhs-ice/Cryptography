import random
from collections import Counter
import string

class MonoalphabeticCipher:
    def __init__(self):
        self.key = self.generate_key()
        self.reverse_key = {v: k for k, v in self.key.items()}
        
    def generate_key(self):
        """Generate random substitution key"""
        letters = list(string.ascii_lowercase)
        shuffled = letters.copy()
        random.shuffle(shuffled)
        return dict(zip(letters, shuffled))
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using substitution cipher"""
        ciphertext = []
        for char in plaintext.lower():
            if char in self.key:
                ciphertext.append(self.key[char])
            else:
                ciphertext.append(char)  # Keep non-alphabet characters
        return ''.join(ciphertext)
    
    def decrypt_with_key(self, ciphertext):
        """Decrypt ciphertext using known key"""
        plaintext = []
        for char in ciphertext.lower():
            if char in self.reverse_key:
                plaintext.append(self.reverse_key[char])
            else:
                plaintext.append(char)
        return ''.join(plaintext)
    
    @staticmethod
    def frequency_attack(ciphertext, lang='english'):
        """Break cipher using frequency analysis"""
        # Standard frequency tables
        freq_tables = {
            'english': {
                'letters': 'etaoinshrdlcumwfgypbvkjxqz',
                'digrams': ['th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt'],
                'trigrams': ['the', 'and', 'ing', 'ion', 'ent', 'her', 'for', 'tha', 'nth', 'int']
            }
        }
        
        # Get letter frequencies in ciphertext
        letters = [c for c in ciphertext.lower() if c.isalpha()]
        freq = Counter(letters)
        total_letters = len(letters)
        
        # Get most common letters in ciphertext
        cipher_freq = [item[0] for item in freq.most_common()]
        
        # Create initial mapping (cipher -> plain)
        mapping = {}
        std_letters = freq_tables[lang]['letters']
        for i in range(min(len(cipher_freq), len(std_letters))):
            mapping[cipher_freq[i]] = std_letters[i]
        
        # Improve mapping using digrams
        digrams = Counter(ciphertext[i:i+2] for i in range(len(ciphertext)-1))
        common_digram = digrams.most_common(1)[0][0]
        if len(common_digram) == 2 and common_digram[0] in mapping and mapping[common_digram[0]] == 't':
            mapping[common_digram[1]] = 'h'  # th
            
        # Improve mapping using trigrams
        trigrams = Counter(ciphertext[i:i+3] for i in range(len(ciphertext)-2))
        common_trigram = trigrams.most_common(1)[0][0]
        if len(common_trigram) == 3 and common_trigram[:2] == common_digram:
            mapping[common_trigram[2]] = 'e'  # the
            
        # Decrypt using current mapping
        decrypted = []
        for char in ciphertext.lower():
            if char in mapping:
                decrypted.append(mapping[char])
            elif char.isalpha():
                decrypted.append('?')  # Unknown
            else:
                decrypted.append(char)  # Punctuation
        
        return ''.join(decrypted), mapping

# Example usage
if __name__ == "__main__":
    print("=== Mono-alphabetic Cipher ===")
    
    # 1. Create cipher and generate key
    cipher = MonoalphabeticCipher()
    print("Generated Key:", cipher.key)
    
    # 2. Encrypt a message
    plaintext = "The quick brown fox jumps over the lazy dog."
    ciphertext = cipher.encrypt(plaintext)
    print("\nPlaintext:", plaintext)
    print("Encrypted:", ciphertext)
    
    # 3. Decrypt with known key
    decrypted = cipher.decrypt_with_key(ciphertext)
    print("\nDecrypted with key:", decrypted)
    
    # 4. Frequency attack (without knowing the key)
    print("\nAttempting to break cipher with frequency analysis...")
    cracked, mapping = MonoalphabeticCipher.frequency_attack(ciphertext)
    print("Recovered Mapping:", mapping)
    print("Cracked Message:", cracked)