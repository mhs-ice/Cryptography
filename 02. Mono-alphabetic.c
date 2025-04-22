#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define ALPHABET_SIZE 26

// Key for substitution (randomly generated)
char key[ALPHABET_SIZE + 1]; // +1 for null terminator

// English letter frequencies (approximate)
const float english_freq[ALPHABET_SIZE] = {
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, // a-e
    0.02228, 0.02015, 0.06094, 0.06966, 0.00153, // f-j
    0.00772, 0.04025, 0.02406, 0.06749, 0.07507, // k-o
    0.01929, 0.00095, 0.05987, 0.06327, 0.09056, // p-t
    0.02758, 0.00978, 0.02360, 0.00150, 0.01974, // u-y
    0.00074  // z
};

// Generate a random substitution key
void generate_key() {
    char alphabet[ALPHABET_SIZE + 1] = "abcdefghijklmnopqrstuvwxyz";
    srand(time(0)); // Seed for randomness
    
    // Fisher-Yates shuffle to randomize the key
    for (int i = ALPHABET_SIZE - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        char temp = alphabet[i];
        alphabet[i] = alphabet[j];
        alphabet[j] = temp;
    }
    strcpy(key, alphabet);
}

// Encrypt using the substitution key
void encrypt(const char *plaintext, char *ciphertext) {
    for (int i = 0; plaintext[i] != '\0'; i++) {
        if (isalpha(plaintext[i])) {
            char lower_char = tolower(plaintext[i]);
            ciphertext[i] = islower(plaintext[i]) 
                ? key[lower_char - 'a'] 
                : toupper(key[lower_char - 'a']);
        } else {
            ciphertext[i] = plaintext[i]; // Non-alphabetic chars remain unchanged
        }
    }
    ciphertext[strlen(plaintext)] = '\0';
}

// Decrypt using the substitution key
void decrypt(const char *ciphertext, char *plaintext) {
    for (int i = 0; ciphertext[i] != '\0'; i++) {
        if (isalpha(ciphertext[i])) {
            char lower_char = tolower(ciphertext[i]);
            for (int j = 0; j < ALPHABET_SIZE; j++) {
                if (key[j] == lower_char) {
                    plaintext[i] = islower(ciphertext[i]) 
                        ? ('a' + j) 
                        : toupper('a' + j);
                    break;
                }
            }
        } else {
            plaintext[i] = ciphertext[i];
        }
    }
    plaintext[strlen(ciphertext)] = '\0';
}

// Perform frequency analysis on ciphertext
void frequency_analysis(const char *ciphertext, float *freq) {
    int counts[ALPHABET_SIZE] = {0};
    int total_letters = 0;

    for (int i = 0; ciphertext[i] != '\0'; i++) {
        if (isalpha(ciphertext[i])) {
            counts[tolower(ciphertext[i]) - 'a']++;
            total_letters++;
        }
    }

    for (int i = 0; i < ALPHABET_SIZE; i++) {
        freq[i] = (total_letters > 0) ? (float)counts[i] / total_letters : 0;
    }
}

// Attempt to break the cipher using frequency analysis
void break_cipher(const char *ciphertext, char *guessed_plaintext) {
    float cipher_freq[ALPHABET_SIZE];
    frequency_analysis(ciphertext, cipher_freq);

    // Find the most frequent letters in ciphertext and map to English frequencies
    int cipher_order[ALPHABET_SIZE];
    int english_order[ALPHABET_SIZE];

    for (int i = 0; i < ALPHABET_SIZE; i++) {
        cipher_order[i] = i;
        english_order[i] = i;
    }

    // Sort cipher frequencies (descending)
    for (int i = 0; i < ALPHABET_SIZE - 1; i++) {
        for (int j = i + 1; j < ALPHABET_SIZE; j++) {
            if (cipher_freq[cipher_order[i]] < cipher_freq[cipher_order[j]]) {
                int temp = cipher_order[i];
                cipher_order[i] = cipher_order[j];
                cipher_order[j] = temp;
            }
        }
    }

    // Sort English frequencies (descending)
    for (int i = 0; i < ALPHABET_SIZE - 1; i++) {
        for (int j = i + 1; j < ALPHABET_SIZE; j++) {
            if (english_freq[english_order[i]] < english_freq[english_order[j]]) {
                int temp = english_order[i];
                english_order[i] = english_order[j];
                english_order[j] = temp;
            }
        }
    }

    // Create a guessed mapping
    char mapping[ALPHABET_SIZE];
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        mapping[cipher_order[i]] = 'a' + english_order[i];
    }

    // Apply the guessed mapping to decrypt
    for (int i = 0; ciphertext[i] != '\0'; i++) {
        if (isalpha(ciphertext[i])) {
            char lower_char = tolower(ciphertext[i]);
            guessed_plaintext[i] = islower(ciphertext[i]) 
                ? mapping[lower_char - 'a'] 
                : toupper(mapping[lower_char - 'a']);
        } else {
            guessed_plaintext[i] = ciphertext[i];
        }
    }
    guessed_plaintext[strlen(ciphertext)] = '\0';
}

int main() {
    char plaintext[1000], ciphertext[1000], decrypted[1000], guessed_plaintext[1000];
    
    generate_key();
    printf("Generated Key: %s\n", key);

    printf("Enter plaintext: ");
    fgets(plaintext, sizeof(plaintext), stdin);
    plaintext[strcspn(plaintext, "\n")] = '\0'; // Remove newline

    encrypt(plaintext, ciphertext);
    printf("\nEncrypted: %s\n", ciphertext);

    decrypt(ciphertext, decrypted);
    printf("Decrypted: %s\n", decrypted);

    break_cipher(ciphertext, guessed_plaintext);
    printf("\nFrequency Analysis Attack Result:\n%s\n", guessed_plaintext);

    return 0;
}