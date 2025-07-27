import string

# Load a basic English word list
def load_dictionary():
    try:
        with open("/usr/share/dict/words") as f:
            words = set(word.strip().lower() for word in f)
    except FileNotFoundError:
        # If dictionary file is not found, fallback to a small list
        words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
            'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there',
            'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get',
            'which', 'go', 'me', 'hasem', 'ali', 'meet', 'pm'
        }
    return words

# Caesar decrypt with a given shift
def caesar_decrypt(ciphertext, shift):
    decrypted = ''
    for char in ciphertext:
        if char.isupper():
            decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        elif char.islower():
            decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            decrypted += char  # Leave punctuation, digits unchanged
    return decrypted

# Count how many real English words are in the decrypted message
def count_english_words(text, dictionary):
    words = text.lower().split()
    count = 0
    for word in words:
        word_clean = ''.join(c for c in word if c in string.ascii_lowercase)  # strip punctuations
        if word_clean in dictionary:
            count += 1
    return count

def auto_crack_caesar(ciphertext):
    dictionary = load_dictionary()
    best_match = ''
    best_score = 0
    best_shift = 0

    print("Trying all 26 Caesar shifts with dictionary scoring...\n")

    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        score = count_english_words(decrypted, dictionary)
        print(f"Shift {shift:2}: {decrypted}  | Score: {score}")
        if score > best_score:
            best_score = score
            best_match = decrypted
            best_shift = shift

    print("\n====== Best Guess Based on Dictionary ======")
    print(f"Best Shift  : {best_shift}")
    print(f"Decrypted   : {best_match}")
    print("============================================")

def main():
    ciphertext = input("Enter Caesar-encrypted message: ")
    auto_crack_caesar(ciphertext)

if __name__ == "__main__":
    main()
