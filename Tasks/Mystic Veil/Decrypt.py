s_box = [(i * 17) % 256 for i in range(256)]
inv_s_box = [0] * 256
for i in range(256):
    inv_s_box[s_box[i]] = i

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def bytes_to_matrix(block):
    return [list(block[i*4:(i+1)*4]) for i in range(4)]

def matrix_to_bytes(matrix):
    return bytes([b for row in matrix for b in row])

def inv_sub_bytes(matrix):
    return [[inv_s_box[b] for b in row] for row in matrix]

def inv_shift_rows(matrix):
    return [row[-i:] + row[:-i] for i, row in enumerate(matrix)]

def add_round_key(matrix, key_matrix):
    return [[b ^ k for b, k in zip(row, key_row)] for row, key_row in zip(matrix, key_matrix)]

def derive_round_keys(key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes.")
    k0 = key
    k1 = key[4:] + key[:4]
    k2 = key[8:] + key[:8]
    return k0, k1, k2

def decrypt_block(block, round_keys):
    matrix = bytes_to_matrix(block)
    matrix = add_round_key(matrix, bytes_to_matrix(round_keys[2]))
    matrix = inv_shift_rows(matrix)
    matrix = inv_sub_bytes(matrix)
    matrix = add_round_key(matrix, bytes_to_matrix(round_keys[1]))
    matrix = inv_shift_rows(matrix)
    matrix = inv_sub_bytes(matrix)
    matrix = add_round_key(matrix, bytes_to_matrix(round_keys[0]))
    return matrix_to_bytes(matrix)

def decrypt_data(ciphertext, key):
    round_keys = derive_round_keys(key)
    plaintext = b""
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        plaintext += decrypt_block(block, round_keys)
    return unpad(plaintext)

key = b'EncryptThisNow!!'

with open("C:/Users/jahna/Downloads/image.jpg.thmh", "rb") as f:
    encrypted_data = f.read()

decrypted_data = decrypt_data(encrypted_data, key)

with open("image_decrypted.jpg", "wb") as f:
    f.write(decrypted_data)

print("Decryption complete. Decrypted file saved as image_decrypted.jpg")
