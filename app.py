# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import string
app = Flask(__name__)

def vigenere_encrypt(plain_text, key):
    key_repeated = (key * (len(plain_text) // len(key) + 1))[:len(plain_text)]
    encrypted_text = ""
    for p, k in zip(plain_text, key_repeated):
        if p.isalpha():
            shift = ord(k.upper()) - ord('A')
            if p.isupper():
                encrypted_text += chr((ord(p) + shift - ord('A')) % 26 + ord('A'))
            else:
                encrypted_text += chr((ord(p) + shift - ord('a')) % 26 + ord('a'))
        else:
            encrypted_text += p
    return encrypted_text

def vigenere_decrypt(encrypted_text, key):
    key_repeated = (key * (len(encrypted_text) // len(key) + 1))[:len(encrypted_text)]
    decrypted_text = ""
    for p, k in zip(encrypted_text, key_repeated):
        if p.isalpha():
            shift = ord(k.upper()) - ord('A')
            if p.isupper():
                decrypted_text += chr((ord(p) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_text += chr((ord(p) - shift - ord('a')) % 26 + ord('a'))
        else:
            decrypted_text += p
    return decrypted_text

def polybius_encrypt(text):
    polybius_square = [
        ['A', 'B', 'C', 'D', 'E'],
        ['F', 'G', 'H', 'I', 'K'],
        ['L', 'M', 'N', 'O', 'P'],
        ['Q', 'R', 'S', 'T', 'U'],
        ['V', 'W', 'X', 'Y', 'Z']
    ]
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            char = char.upper()
            if char == 'J':
                char = 'I'
            for i, row in enumerate(polybius_square):
                if char in row:
                    encrypted_text += str(i + 1) + str(row.index(char) + 1)
        else:
            encrypted_text += char
    return encrypted_text

def polybius_decrypt(text):
    polybius_square = [
        ['A', 'B', 'C', 'D', 'E'],
        ['F', 'G', 'H', 'I', 'K'],
        ['L', 'M', 'N', 'O', 'P'],
        ['Q', 'R', 'S', 'T', 'U'],
        ['V', 'W', 'X', 'Y', 'Z']
    ]
    decrypted_text = ""
    i = 0
    while i < len(text):
        if text[i].isdigit():
            row = int(text[i])
            col = int(text[i + 1])
            decrypted_text += polybius_square[row - 1][col - 1]
            i += 2
        else:
            decrypted_text += text[i]
            i += 1
    return decrypted_text

def reverse_text(text):
    return text[::-1]


def decimal_to_base36(decimal_number):
    """Converts a decimal number to its base-36 representation."""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base36_string = ""
    while decimal_number > 0:
        remainder = decimal_number % 36
        base36_string = digits[remainder] + base36_string  # Append digits in reverse order
        decimal_number //= 36
    return base36_string

def base36_to_decimal(base36_string):
    """Converts a base-36 string to its decimal equivalent."""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    decimal_number = 0
    power = 0
    for digit in base36_string[::-1]:  # Iterate through digits in reverse order
        decimal_number += digits.index(digit) * (36 ** power)  # Multiply by corresponding power of 36
        power += 1
    return decimal_number

# Get user input
plain_text = input("Enter the plain text: ")
key = input("Enter the Vigenere key: ")

# Encrypt using Vigenere cipher
vigenere_encrypted = vigenere_encrypt(plain_text, key)

# Encrypt using Polybius cipher
polybius_encrypted = polybius_encrypt(vigenere_encrypted)

# Convert to integer
polybius_encrypted = int(polybius_encrypted)

#Polybius to Base36
base36_string = decimal_to_base36(polybius_encrypted)

# Convert back to decimal
original_decimal = base36_to_decimal(base36_string)

# Decrypt Polybius cipher
polybius_decrypted = polybius_decrypt(str(original_decimal))

# Decrypt Vigenere cipher
vigenere_decrypted = vigenere_decrypt(polybius_decrypted, key)

# # Display results
# print("\nOriginal Text          :", plain_text)
# print("Vigenere Encrypted Text:", vigenere_encrypted)
# print("Polybius Encrypted Text:", polybius_encrypted)
# print("Base36 Encrypted Text  :", base36_string)
# print("\nDecrypted Base36 Text  :", original_decimal)
# print("Decrypted Polybius Text:", polybius_decrypted)
# print("Decrypted Vigenere Text:", vigenere_decrypted)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt_data', methods=['POST'])
def encrypt_data():
    left_text = request.form['leftText']
    left_key = request.form['leftKey']

    # Perform encryption
    vigenere_encrypted = vigenere_encrypt(left_text, left_key)
    polybius_encrypted = polybius_encrypt(vigenere_encrypted)
    base36_string = decimal_to_base36(int(polybius_encrypted))

    # Convert to decimal for display
    original_decimal = base36_to_decimal(base36_string)

    # Decrypt Polybius cipher
    polybius_decrypted = polybius_decrypt(str(original_decimal))

    # Decrypt Vigenere cipher
    vigenere_decrypted = vigenere_decrypt(polybius_decrypted, left_key)

    return render_template('index.html',
                           left_text=left_text,
                           left_key=left_key,
                           vigenere_encrypted=vigenere_encrypted,
                           polybius_encrypted=polybius_encrypted,
                           base36_string=base36_string,
                           original_decimal=original_decimal,
                           polybius_decrypted=polybius_decrypted,
                           vigenere_decrypted=vigenere_decrypted)


if __name__ == '__main__':
    app.run(debug=True)