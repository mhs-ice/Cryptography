import random
from collections import Counter
import matplotlib.pyplot as plt

def generate_key():
    """Generate a random substitution key"""
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    shuffled = alphabet.copy()
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def invert_key(key):
    """Generate inverse key for decryption"""
    return {v: k for k, v in key.items()}

def monoalphabetic_encrypt(plaintext, key):
    """Encrypt plaintext using mono-alphabetic substitution"""
    ciphertext = []
    for char in plaintext.lower():
        if char in key:
            ciphertext.append(key[char])
        else:
            ciphertext.append(char)  # Keep non-alphabet characters
    return ''.join(ciphertext)

def monoalphabetic_decrypt(ciphertext, key):
    """Decrypt ciphertext using mono-alphabetic substitution"""
    inverse_key = invert_key(key)
    plaintext = []
    for char in ciphertext.lower():
        if char in inverse_key:
            plaintext.append(inverse_key[char])
        else:
            plaintext.append(char)
    return ''.join(plaintext)

def frequency_analysis(text):
    """Perform frequency analysis on text"""
    letters = [c for c in text.lower() if c.isalpha()]
    freq = Counter(letters)
    total = len(letters)
    return {char: count/total for char, count in freq.items()}

def plot_frequencies(plain_freq, cipher_freq):
    """Plot frequency distributions"""
    plt.figure(figsize=(12, 6))
    
    # Plaintext frequencies
    plt.subplot(1, 2, 1)
    plt.bar(plain_freq.keys(), plain_freq.values())
    plt.title("Plaintext Letter Frequencies")
    
    # Ciphertext frequencies
    plt.subplot(1, 2, 2)
    plt.bar(cipher_freq.keys(), cipher_freq.values())
    plt.title("Ciphertext Letter Frequencies")
    
    plt.tight_layout()
    plt.show()

def break_substitution(ciphertext, reference_freq):
    """Attempt to break substitution cipher using frequency analysis"""
    cipher_freq = frequency_analysis(ciphertext)
    
    # Sort frequencies from highest to lowest
    sorted_ref = sorted(reference_freq.items(), key=lambda x: -x[1])
    sorted_cipher = sorted(cipher_freq.items(), key=lambda x: -x[1])
    
    # Create mapping based on frequency order
    mapping = {}
    for (cipher_char, _), (ref_char, _) in zip(sorted_cipher, sorted_ref):
        mapping[cipher_char] = ref_char
    
    # Apply the mapping to decrypt
    decrypted = []
    for char in ciphertext.lower():
        if char in mapping:
            decrypted.append(mapping[char])
        else:
            decrypted.append(char)
    
    return ''.join(decrypted), mapping

# English letter frequency reference (from Wikipedia)
ENGLISH_FREQ = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
    'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
    'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
    'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
    'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
    'y': 0.01974, 'z': 0.00074
}

def main():
    # Generate a random substitution key
    key = generate_key()
    print("Substitution Key:", key)
    
    # Get user input
    plaintext = input("Enter plaintext to encrypt: ")
    
    # Encrypt
    ciphertext = monoalphabetic_encrypt(plaintext, key)
    print("\nEncrypted:", ciphertext)
    
    # Decrypt
    decrypted = monoalphabetic_decrypt(ciphertext, key)
    print("Decrypted:", decrypted)
    
    # Frequency analysis
    plain_freq = frequency_analysis(plaintext)
    cipher_freq = frequency_analysis(ciphertext)
    
    # Plot frequencies
    plot_frequencies(plain_freq, cipher_freq)
    
    # Attempt to break the cipher
    print("\nAttempting to break the cipher using frequency analysis...")
    guessed_plaintext, mapping = break_substitution(ciphertext, ENGLISH_FREQ)
    print("\nGuessed mapping:", mapping)
    print("Guessed plaintext:", guessed_plaintext)

if __name__ == "__main__":
    main()