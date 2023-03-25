def encrypt(string: str, n: int = 3):
    b = ""
    previous_code = 0
    for (index, i) in enumerate(string):
        code_of_i = ord(i)
        new_code = code_of_i + n + index + previous_code
        previous_code = code_of_i
        new_i = chr(new_code)
        b += new_i

    return b


def decrypt(string: str, n: int = 3) -> str:
    b = ""
    previous_code = 0
    for (index, i) in enumerate(string):
        code_of_i = ord(i)
        new_code = code_of_i - n - index - previous_code
        previous_code = new_code
        new_i = chr(new_code)
        b += new_i

    return b


a = "test"

encrypted = encrypt(a)
print(encrypted)
decrypted = decrypt(encrypted)
print(decrypted)
