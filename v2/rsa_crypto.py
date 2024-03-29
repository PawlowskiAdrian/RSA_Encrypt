from Crypto.PublicKey import RSA  # to generate RSA keys, work with enc/dec
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random  # to generate random numbers
import base64  # to work with bytes

ENCRYPTION_SIZE_MULTIPLIER = 8

key_path = "00001-key"
encryption_size = 256 * max(int(ENCRYPTION_SIZE_MULTIPLIER), 4)


def _key_open_RSAPair():
    try:
        priv_key = None
        file = open(key_path + ".key", "rb")
        priv_key = file.read()
        file.close()
        priv_key = RSA.importKey(priv_key)  # set private key in mem

        file = open(key_path + ".pub", "rb")
        pub_key = file.read()
        file.close()
        pub_key = RSA.importKey(pub_key)  # set public key in mem

    except FileNotFoundError:
        # generate RSA key pair
        if priv_key is None:
            priv_key = RSA.generate(encryption_size, Random.new().read)
        pub_key = priv_key.publickey()
        # ? export keys to bytes
        priv_key_bytes = priv_key.exportKey()
        pub_key_bytes = pub_key.exportKey()

        # create file and write to it key (bytes)
        with open(key_path + ".key", "wb") as fp:
            fp.write(
                priv_key_bytes
            )  # saves priv key to file @ self._key_path "ex.: ./key.key"
            fp.close()
        with open(key_path + ".pub", "wb") as fp:
            fp.write(
                pub_key_bytes
            )  #! OVERWRITES ANY PUB KEY WITH SAME FILE NAME "ex.: ./key"
            fp.close()
        pass
    return priv_key, pub_key


def _key_open_RSAPriv():
    try:
        priv_key = None
        file = open(key_path + ".key", "rb")
        priv_key = file.read()
        file.close()
        priv_key = RSA.importKey(priv_key)  # set private key in mem

    except FileNotFoundError:
        # generate RSA key pair
        priv_key = RSA.generate(encryption_size, Random.new().read)
        # ? export keys to bytes
        priv_key_bytes = priv_key.exportKey()

        # create file and write to it key (bytes)
        with open(key_path + ".key", "wb") as fp:
            fp.write(
                priv_key_bytes
            )  # saves priv key to file @ self._key_path "ex.: ./key.key"
            fp.close()
        pass
    return priv_key


def _key_open_RSAPub():
    try:
        pub_key = None
        file = open(key_path + ".pub", "rb")
        pub_key = file.read()
        file.close()
        pub_key = RSA.importKey(pub_key)  # set public key in mem

    except FileNotFoundError:
        # generate RSA key pair
        priv_key, pub_key = _key_open_RSAPair()
    return pub_key


def decrypt_rsa(c2, private_key_rsa):  # aka. priv key AES
    encryptor = PKCS1_OAEP.new(private_key_rsa)
    decrypted = encryptor.decrypt(c2)  # decrypted bytes
    return base64.b64decode(decrypted)


def encrypt_rsa(private_key_aes, public_key_rsa):  # output = C2
    """
    RSA maximum bytes to encrypt, comparison to AES in terms of ,
    RSA, as defined by PKCS#1, encrypts "messages" of limited size.
    the maximum size of data which can be encrypted with RSA is 245 bytes.
    To get the size of the modulus of an RSA key call the function RSA_size.
    The modulus size is the key size in bits / 8.
    Thus a 1024-bit RSA key using OAEP padding can encrypt up to (1024/8) – 42 = 128 – 42 = 86 bytes.
    A 2048-bit key can encrypt up to (2048/8) – 42 = 256 – 42 = 214 bytes.
    """
    # max_size_bytes= int(min(4096/8-42),245)
    # encrypt data ( data -> encode -> encrypt )
    encoded = base64.b64encode(private_key_aes)
    encryptor = PKCS1_OAEP.new(public_key_rsa)
    return encryptor.encrypt(encoded)  # encrypt
