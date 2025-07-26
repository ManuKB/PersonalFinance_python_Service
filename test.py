from cryptography.fernet import Fernet

# Generate and store this key securely (e.g., env var)
key = Fernet.generate_key()
# key = "7o_bgHxK0mCWBq1-1X4qkbIWqkkk3IYNmiatHtHII3w="
print(f"Key: {key.decode()}")  # Store this key securely
cipher = Fernet(key)

# Encrypt
#token = "secret_token_123"
#encrypted = cipher.encrypt(token.encode())

encrypted =b'gAAAAABodn7Da6Kq3jOfMqz5wXdVS6wah97rmZMT8M0QajlHihYeE6VOrLAAm_1pJNFYyM0C-VBKF5t9hLFTnek6ROhu9A7J2W5zeQvWxjHxlI70oeL8Bto='

print(f"Encrypted: {encrypted}")

# Decrypt
decrypted = cipher.decrypt(encrypted).decode()


print(f"Decrypted: {decrypted}")