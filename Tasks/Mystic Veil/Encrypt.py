s_box = [ (i * 17) % 256 for i in range(256) ]
inv_s_box = [0] * 256
for i in range(256):
    inv_s_box[s_box[i]] = i

def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def bytes_to_matrix(block):
    return [list(block[i*4:(i+1)*4]) for i in range(4)]

def matrix_to_bytes(matrix):
    return bytes([b for row in matrix for b in row])

def sub_bytes(matrix):
    return [[s_box[b] for b in row] for row in matrix]

def shift_rows(matrix):
    return [row[i:] + row[:i] for i, row in enumerate(matrix)]

def add_round_key(matrix, key_matrix):
    return [[b ^ k for b, k in zip(row, key_row)] for row, key_row in zip(matrix, key_matrix)]

def derive_round_keys(key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes.")
    k0 = key
    k1 = key[4:] + key[:4]
    k2 = key[8:] + key[:8]
    return k0, k1, k2

def encrypt_block(block, round_keys):
    matrix = bytes_to_matrix(block)
    matrix = add_round_key(matrix, bytes_to_matrix(round_keys[0]))
    matrix = sub_bytes(matrix)
    matrix = shift_rows(matrix)
    matrix = add_round_key(matrix, bytes_to_matrix(round_keys[1]))
    matrix = sub_bytes(matrix)
    matrix = shift_rows(matrix)
    matrix = add_round_key(matrix, bytes_to_matrix(round_keys[2]))
    return matrix_to_bytes(matrix)

def encrypt_data(data, key):
    padded_data = pad(data)
    round_keys = derive_round_keys(key)
    ciphertext = b""
    for i in range(0, len(padded_data), 16):
        block = padded_data[i:i+16]
        ciphertext += encrypt_block(block, round_keys)
    return ciphertext

key = b'EncryptThisNow!!'

with open("image.jpg", "rb") as f:
    input_data = f.read()

ciphertext = encrypt_data(input_data, key)
encrypted_filename = "image.jpg.thmh"
with open(encrypted_filename, "wb") as f:
    f.write(ciphertext)

print(f"Encryption complete. Encrypted file saved as {encrypted_filename}")