import os
from v2.rsa_crypto import _key_open_RSAPair
from v2.aes_crypto import _key_open_AESPriv

# module path to keys
key_path = "00001-key"

# RSA specific data
ENCRYPTION_SIZE_MULTIPLIER = 8 # 8 will create 2048 RSA
encryption_size = 256 * max(int(ENCRYPTION_SIZE_MULTIPLIER), 4)

# AES specific data
aes_password = os.getenv("AES_PRIVATE_KEY_PASSWORD")
if aes_password is None:
    aes_password = "apd4XNPn5t6GDtzzJbfZLsHFEPUvFEfkxCng9wwJm5DD"
aes_salt = os.getenv("AES_PRIVATE_KEY_SALT")
if aes_salt is None:
    aes_salt = "SALTGDtzzJFORHFEPUvFEfAES9wwJisHEREm5DD"

# Create RSA key pair and AES priv
_key_open_RSAPair()
_key_open_AESPriv()