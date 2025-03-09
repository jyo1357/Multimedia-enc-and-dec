from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import base64
import io
import numpy as np
import os
from django.conf import settings
class AESEncryption:
    def __init__(self, key):
        self.key = key.ljust(32)[:32]  # Ensure key is 32 bytes

    def encrypt(self, raw_text):
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_ECB)
        padded_text = raw_text.ljust(32)[:32]
        encrypted_bytes = cipher.encrypt(padded_text.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, enc_text):
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_ECB)
        decoded_bytes = base64.b64decode(enc_text)
        decrypted_bytes = cipher.decrypt(decoded_bytes).strip()
        return decrypted_bytes.decode('utf-8')


# Constants for encryption
BLOCK_SIZE = 16
SALT_SIZE = 16

# Pad function for AES using PKCS7 padding
def pad_data(data):
    return pad(data, BLOCK_SIZE)

# Derive a key using PBKDF2 (Password-Based Key Derivation)
def derive_key(password, salt):
    return PBKDF2(password.encode(), salt, dkLen=BLOCK_SIZE)

# Encrypt file using password (AES with CBC mode)
def encrypt_file(input_path, output_path, password):
    salt = get_random_bytes(SALT_SIZE)  # Generate a random salt
    key = derive_key(password, salt)  # Derive key from password
    iv = get_random_bytes(BLOCK_SIZE)  # Generate a random IV for CBC mode

    with open(input_path, 'rb') as f:
        plaintext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad_data(plaintext))

    with open(output_path, 'wb') as f:
        f.write(salt)  # Write the salt at the start of the file
        f.write(iv)  # Write the IV for CBC mode
        f.write(ciphertext)

# Decrypt file using password
def decrypt_file(input_path, output_path, password):
    with open(input_path, 'rb') as f:
        salt = f.read(SALT_SIZE)  # Extract the salt
        iv = f.read(BLOCK_SIZE)  # Extract the IV
        ciphertext = f.read()  # Read the encrypted content

    key = derive_key(password, salt)  # Derive key from password
    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

    with open(output_path, 'wb') as f:
        f.write(plaintext)

# Encrypt image using a standard AES algorithm
def encrypt_image(image_path, key, size=(500, 500)):
    """Encrypts the image using a chaos-based algorithm and resizes it."""
    img = Image.open(image_path)
    img = img.resize(size)  # Resize the image to reduce file size
    img_array = np.array(img)
    encrypted_path = os.path.join(settings.MEDIA_ROOT, 'encrypted_images', os.path.basename(image_path))
    # Chaos-based encryption using XOR and key scrambling
    np.random.seed(sum(ord(c) for c in key))
    random_map = np.random.randint(0, 256, img_array.shape, dtype=np.uint8)
    encrypted_array = img_array ^ random_map

    encrypted_image = Image.fromarray(encrypted_array)
    encrypted_image_path = f"{os.path.splitext(image_path)[0]}_encrypted.png"
    encrypted_image.save(encrypted_image_path, format='PNG')  # Saving as PNG to ensure compression

    return encrypted_image_path



def decrypt_image_to_base64(encrypted_image_path, key):
    # Open the encrypted image
    encrypted_img = Image.open(encrypted_image_path)
    encrypted_array = np.array(encrypted_img)

    # Apply chaos-based decryption (just an example, you can modify this)
    np.random.seed(sum(ord(c) for c in key))  # Using the key for reproducibility
    random_map = np.random.randint(0, 256, encrypted_array.shape, dtype=np.uint8)
    decrypted_array = encrypted_array ^ random_map

    # Create a decrypted image
    decrypted_image = Image.fromarray(decrypted_array)
    # Convert the decrypted image to a base64 string
    buffered = io.BytesIO()
    decrypted_image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')  # Convert to base64 string

    return img_base64

# Encrypt file using password (AES with CBC mode)
# Encrypt audio file using password (AES with CBC mode)
# Encrypt audio file using password (AES with CBC mode)
def encrypt_audio(input_path, output_path, password):
    salt = get_random_bytes(SALT_SIZE)  # Generate a random salt
    key = derive_key(password, salt)  # Derive key from password
    iv = get_random_bytes(BLOCK_SIZE)  # Generate a random IV for CBC mode

    with open(input_path, 'rb') as f:
        plaintext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad_data(plaintext))

    with open(output_path, 'wb') as f:
        f.write(salt)  # Write the salt at the start of the file
        f.write(iv)  # Write the IV for CBC mode
        f.write(ciphertext)

# Decrypt file using password
def decrypt_audio(input_path, output_path, password):
    with open(input_path, 'rb') as f:
        salt = f.read(SALT_SIZE)  # Extract the salt
        iv = f.read(BLOCK_SIZE)  # Extract the IV
        ciphertext = f.read()  # Read the encrypted content

    key = derive_key(password, salt)  # Derive key from password
    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

    with open(output_path, 'wb') as f:
        f.write(plaintext)

# Encrypt video file using password (AES with CBC mode)
def encrypt_video(input_path, output_path, password):
    salt = get_random_bytes(SALT_SIZE)  # Generate a random salt
    key = derive_key(password, salt)  # Derive key from password
    iv = get_random_bytes(BLOCK_SIZE)  # Generate a random IV for CBC mode

    with open(input_path, 'rb') as f:
        plaintext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad_data(plaintext))

    with open(output_path, 'wb') as f:
        f.write(salt)  # Write the salt at the start of the file
        f.write(iv)  # Write the IV for CBC mode
        f.write(ciphertext)

# Decrypt file using password
def decrypt_video(input_path, output_path, password):
    with open(input_path, 'rb') as f:
        salt = f.read(SALT_SIZE)  # Extract the salt
        iv = f.read(BLOCK_SIZE)  # Extract the IV
        ciphertext = f.read()  # Read the encrypted content

    key = derive_key(password, salt)  # Derive key from password
    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

    with open(output_path, 'wb') as f:
        f.write(plaintext)
