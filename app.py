# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import string
app = Flask(__name__)

def generate_vigenere_key(message, key):
    key = ''.join([key[i % len(key)] for i in range(len(message))])
    return key

def vigenere_encrypt(plaintext, key):
    encrypted_text = ''
    for i in range(len(plaintext)):
        char = plaintext[i]
        if char.isalpha():
            shift = ord(key[i].upper()) - ord('A')
            encrypted_char = chr((ord(char.upper()) + shift - 2 * ord('A')) % 26 + ord('A'))
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def vigenere_decrypt(ciphertext, key):
    decrypted_text = ''
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():
            shift = ord(key[i].upper()) - ord('A')
            decrypted_char = chr((ord(char.upper()) - shift - 2 * ord('A')) % 26 + ord('A'))
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def generate_polybius_table():
    alphabet = string.ascii_uppercase
    table = [['' for _ in range(5)] for _ in range(5)]
    k = 0
    for i in range(5):
        for j in range(5):
            if k < len(alphabet):
                table[i][j] = alphabet[k]
                k += 1
    return table

def polybius_encrypt(plaintext, table):
    encrypted_text = ''
    for char in plaintext:
        if char.isalpha():
            char = char.upper()
            for i in range(5):
                for j in range(5):
                    if table[i][j] == char:
                        encrypted_text += str(i + 1).zfill(2) + str(j + 1).zfill(2)  # Treat two digits as a single number
        else:
            encrypted_text += char
    return encrypted_text

def polybius_decrypt(ciphertext, table):
    decrypted_text = ''
    i = 0
    while i < len(ciphertext):
        if ciphertext[i].isdigit() and ciphertext[i + 1].isdigit():
            row = int(ciphertext[i:i + 2]) - 1
            col = int(ciphertext[i + 2:i + 4]) - 1
            decrypted_text += table[row][col]
            i += 4
        else:
            decrypted_text += ciphertext[i]
            i += 1
    return decrypted_text

def base36_encode(text):
    decimal_value = int.from_bytes(text.encode('utf-8'), 'big')
    return base36_encode_decimal(decimal_value)

def base36_encode_decimal(decimal_value):
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base36 = ''
    while decimal_value:
        decimal_value, remainder = divmod(decimal_value, 36)
        base36 = characters[remainder] + base36
    return base36 or '0'

def base36_decode(text):
    decimal_value = int(text, 36)
    return decimal_value.to_bytes((decimal_value.bit_length() + 7) // 8, 'big').decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html', left_text='', left_key='', encrypted_text='')

@app.route('/encrypt_data', methods=['POST'])
def encrypt_data():
    left_text = request.form['leftText']
    left_key = request.form['leftKey']

    # Perform Vigenere encryption
    vigenere_key_extended = generate_vigenere_key(left_text, left_key)
    vigenere_encrypted = vigenere_encrypt(left_text, vigenere_key_extended)

    # Perform Polybius encryption
    polybius_table = generate_polybius_table()
    polybius_encrypted = polybius_encrypt(vigenere_encrypted, polybius_table)

    # Perform Base36 encoding
    base36_encoded = base36_encode(polybius_encrypted)

    # Render the updated content
    return render_template('index.html', left_text=left_text, left_key=left_key, encrypted_text=base36_encoded)

@app.route('/decrypt_data', methods=['POST'])
def decrypt_data():
    encrypted_text = request.form['rightData']
    left_key = request.form['leftKey']

    # Perform Base36 decoding
    polybius_encrypted = base36_decode(encrypted_text)

    # Perform Polybius decryption
    polybius_table = generate_polybius_table()
    vigenere_encrypted = polybius_decrypt(polybius_encrypted, polybius_table)

    # Perform Vigenere decryption
    vigenere_key_extended = generate_vigenere_key(vigenere_encrypted, left_key)
    decrypted_text = vigenere_decrypt(vigenere_encrypted, vigenere_key_extended)

    # Render the updated content
    return render_template(
        'index.html',
        left_text='',
        left_key=left_key,
        encrypted_text=decrypted_text,  # Pass the decrypted text to the template
        decoded_polybius=polybius_encrypted,  # Pass the Polybius decrypted text to the template
        decoded_vigenere=vigenere_encrypted,  # Pass the Vigenere decrypted text to the template
        decoded_text=decrypted_text  # Pass the final decrypted text to the template
    )


if __name__ == '__main__':
    app.run(debug=True)

