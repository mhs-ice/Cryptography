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
        """Improved frequency analysis attack"""
        # Enhanced frequency tables
        freq_tables = {
            'english': {
                'letter_freq': [
                    ('e', 12.7), ('t', 9.1), ('a', 8.2), ('o', 7.5), ('i', 7.0),
                    ('n', 6.7), ('s', 6.3), ('h', 6.1), ('r', 6.0), ('d', 4.3),
                    ('l', 4.0), ('c', 2.8), ('u', 2.8), ('m', 2.4), ('w', 2.4),
                    ('f', 2.2), ('g', 2.0), ('y', 2.0), ('p', 1.9), ('b', 1.5),
                    ('v', 1.0), ('k', 0.8), ('j', 0.2), ('x', 0.2), ('q', 0.1),
                    ('z', 0.1)
                ],
                'digrams': [
                    'th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt',
                    'ha', 'es', 'st', 'en', 'ed', 'to', 'it', 'ou', 'ea', 'hi',
                    'is', 'or', 'ti', 'as', 'te', 'et', 'ng', 'of', 'al', 'de',
                    'se', 'le', 'sa', 'si', 'ar', 've', 'ra', 'ld', 'ur'
                ],
                'trigrams': [
                    'the', 'and', 'ing', 'ion', 'ent', 'her', 'for', 'tha', 'nth',
                    'int', 'ere', 'tio', 'ter', 'est', 'ers', 'ati', 'hat', 'ate',
                    'all', 'eth', 'hes', 'ver', 'his', 'oft', 'ith', 'fth', 'sth',
                    'oth', 'res', 'ont'
                ]
            }
        }
        
        # Get letter frequencies in ciphertext
        letters = [c for c in ciphertext.lower() if c.isalpha()]
        if not letters:
            return "No alphabetic characters found", {}
            
        freq = Counter(letters)
        total_letters = len(letters)
        
        # Get most common letters in ciphertext (sorted by frequency)
        cipher_freq = [item[0] for item in freq.most_common()]
        
        # Create initial mapping (cipher -> plain)
        mapping = {}
        std_letters = [item[0] for item in freq_tables[lang]['letter_freq']]
        
        # Map most frequent cipher letters to most frequent English letters
        for i in range(min(len(cipher_freq), len(std_letters))):
            mapping[cipher_freq[i]] = std_letters[i]
        
        # Improve mapping using digrams
        digrams = Counter(ciphertext[i:i+2].lower() for i in range(len(ciphertext)-1) 
                   if ciphertext[i].isalpha() and ciphertext[i+1].isalpha())
        
        for digram, _ in digrams.most_common(10):  # Top 10 digrams
            if len(digram) != 2:
                continue
                
            # If we've mapped the first character to 't', second is likely 'h'
            if digram[0] in mapping and mapping[digram[0]] == 't':
                mapping[digram[1]] = 'h'
            
            # Other common digram patterns
            if digram[0] in mapping and mapping[digram[0]] == 'h':
                mapping[digram[1]] = 'e'
            if digram[0] in mapping and mapping[digram[0]] == 'a':
                mapping[digram[1]] = 'n'
        
        # Improve mapping using trigrams
        trigrams = Counter(ciphertext[i:i+3].lower() for i in range(len(ciphertext)-2) 
                    if ciphertext[i].isalpha() and ciphertext[i+1].isalpha() and ciphertext[i+2].isalpha())
        
        for trigram, _ in trigrams.most_common(5):  # Top 5 trigrams
            if len(trigram) != 3:
                continue
                
            # Check for 'the' pattern
            if (trigram[0] in mapping and mapping[trigram[0]] == 't' and
                trigram[1] in mapping and mapping[trigram[1]] == 'h'):
                mapping[trigram[2]] = 'e'
            
            # Check for 'and' pattern
            if (trigram[0] in mapping and mapping[trigram[0]] == 'a' and
                trigram[2] in mapping and mapping[trigram[2]] == 'd'):
                mapping[trigram[1]] = 'n'
        
        # Decrypt using current mapping
        decrypted = []
        for char in ciphertext.lower():
            if char in mapping:
                decrypted.append(mapping[char])
            elif char.isalpha():
                decrypted.append('_')  # Use underscore for unknown letters
            else:
                decrypted.append(char)  # Keep punctuation and spaces
        
        # Additional refinement: look for common words
        decrypted_text = ''.join(decrypted)
        words = decrypted_text.split()
        
        # Try to identify common short words
        for i, word in enumerate(words):
            if len(word) == 1 and word == 'a':
                # Find which cipher letter maps to 'a'
                for c in ciphertext.lower():
                    if c.isalpha() and c in mapping and mapping[c] == 'a':
                        # Look at the original word position
                        orig_word = ciphertext.split()[i]
                        if len(orig_word) == 1:
                            mapping[orig_word[0].lower()] = 'a'
                            break
        
        # Final decryption with improved mapping
        final_decrypted = []
        for char in ciphertext.lower():
            if char in mapping:
                final_decrypted.append(mapping[char])
            elif char.isalpha():
                final_decrypted.append('_')
            else:
                final_decrypted.append(char)
        
        return ''.join(final_decrypted), mapping

# Example usage with longer text for better results
if __name__ == "__main__":
    print("=== Enhanced Mono-alphabetic Cipher Cracker ===")
    
    # Create cipher and generate key
    cipher = MonoalphabeticCipher()
    
    # Use a longer plaintext for better frequency analysis
    plaintext = """The quick brown fox jumps over the lazy dog. This sentence contains all 
    the letters in the English alphabet. Frequency analysis works better with more text. 
    The more words we have, the more accurate our letter frequency counts will be."""
    
    ciphertext = cipher.encrypt(plaintext)
    print("\nPlaintext:", plaintext[:50], "...")
    print("Encrypted:", ciphertext[:50], "...")
    
    # Frequency attack
    print("\nAttempting frequency analysis attack...")
    cracked, mapping = MonoalphabeticCipher.frequency_attack(ciphertext)
    print("\nRecovered Mapping:")
    for c in sorted(mapping.items(), key=lambda x: x[1]):
        print(f"{c[1]} -> {c[0]}")
    
    print("\nCracked Message:")
    print(cracked)
    
    # Compare with actual decryption
    actual_decrypted = cipher.decrypt_with_key(ciphertext)
    print("\nActual Decrypted Message:")
    print(actual_decrypted)