def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    key_length = len(keyword)
    
    for i in range(len(plaintext)):
        char = plaintext[i]
        if char.isalpha():
            key_char = keyword[i % key_length]
            shift = ord(key_char) - ord('A') if key_char.isupper() else ord(key_char) - ord('a')
            
            if char.islower():
                encrypted_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            elif char.isupper():
                encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            encrypted_char = char
        
        ciphertext += encrypted_char

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    
    key_length = len(keyword)
    
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():
            key_char = keyword[i % key_length]
            shift = ord(key_char) - ord('A') if key_char.isupper() else ord(key_char) - ord('a')
            
            if char.islower():
                decrypted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
            elif char.isupper():
                decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
        else:
            decrypted_char = char
        
        plaintext += decrypted_char

    return plaintext
