from Crypto.PublicKey import RSA # to generate RSA keys, work with enc/dec
from Crypto.Cipher import AES # to encrypt and decrypt long messages
from hashlib import sha256 # to work with aes, generates sha256 based on input v1.0
from Crypto.Protocol.KDF import PBKDF2 # to work with aes, generates key better than sha256 of password v2.0
# from Crypto.Cipher.PKCS1_v1_5 import PKCS115_Cipher
from Crypto import Random # to generate random numbers
import base64 # to work with bytes

import os # to work with path on OS
from os.path import join
from os import getcwd
from dotenv import load_dotenv

# By default RSA requires min. 256*4 size, so any value set below 4 will be set to 4 by default

dotenv_path = join(getcwd(), '.aes_psw') ## stored in .env file
load_dotenv(dotenv_path)

#TODO: implement password generator

class Encryptor:
    def __init__(self,message=None,c1=None,c2=None,mode=None,key_path=None,encryption_size_multiplier=None,aes_password=None,aes_salt=None):
        try:
            # RSA PART
            self.__priv_key_RSA=None
            self.__pub_key_RSA=None
            if encryption_size_multiplier is not None: # encryption key size <-- force to create NEW key pairs
                self.__encryption_size=256*max(int(encryption_size_multiplier),4)
                self.__key_path = self._find_key_path()
            else:
                if key_path is not None: # specified custom key, if not -> create new key pair with default values
                    self.__key_path = str(key_path) # holds path to key file
                else:
                    self.__key_path = self._find_key_path()
                    self.__encryption_size=256*16 # this will be executed only if key_path=None AND encryption_size=None
            # AES PART 256-bit encryption
            self.__priv_key_AES=None
            self.__BLOCK_SIZE = 16
            self.__pad = lambda s,BLOCK_SIZE: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
            self.__unpad = lambda s: s[:-ord(s[len(s) - 1:])]
            self.__message=message # message to encrypt
            self.__c1=c1 # message to decrypt
            self.__c2=c2 # encrypted aes priv key
            
            if aes_password is not None:
                self.__aes_password = str(aes_password)
            else:
                self.__aes_password = os.getenv('AES_PRIVATE_KEY_PASSWORD')
            if self.__aes_password is None:
                self.__aes_password = 'apd4XNPn5t6GDtzzJbfZLsHFEPUvFEfkxCng9wwJm5DD'

            if aes_salt is not None:
                self.__aes_salt = str(aes_salt)
            else:
                self.__aes_salt = os.getenv('AES_SALT')
            if self.__aes_salt is None:
                self.__aes_salt = 'SALTGDtzzJFORHFEPUvFEfAES9wwJisHEREm5DD'

        except:
            print('Error occured!\n \
                message = str\n \
                key_path = not required, full path to .key & .pub file (same name required)\n \
                encryption_size_multiplier = integer >= 4\n \
                aes_password = str, used for creating aes private key')

    def _find_key_path(self):
        path_finder=None
        increment=1
        while(path_finder==None):
            try:
                path_finder = "%s-key" %(str(increment).zfill(5))
                file = open(path_finder, 'rb') # exception or NOT
                file.close() # finds first not set filename for .key
                #!!! IT WILL OVERWRITE .pub and .aes FILES !!!
            except FileNotFoundError:
                increment+=1 
                continue
        return path_finder

    def __pbkdf2_for_aes(self,password,salt):
        salt = bytes(salt,'utf-8')
        kdf = PBKDF2(password,salt,64,1000)
        key= kdf[:32]
        return key

    def _key_open_AESPriv(self):
        try:
            private_key_aes = None
            file = open(self.__key_path+".aes", 'rb')
            private_key_aes = file.read()
            file.close()

        except FileNotFoundError:
            # generate AES private key based on high entrophy self generated password
            # private_key_aes = sha256(self.__aes_password.encode("utf-8")).digest() # this was v1.0
            private_key_aes = self.__pbkdf2_for_aes(self.__aes_password,self.__aes_salt) # this is v2.0

            with open(self.__key_path+".aes", 'wb') as fp:
                fp.write(private_key_aes) # saves priv key to file @ self._key_path "ex.: ./key.key"
                fp.close()
            pass
        if private_key_aes is not None:
            self.__priv_key_AES = private_key_aes
        return private_key_aes

    def _key_open_RSAPriv(self):
        try:
            priv_key = None
            file = open(self.__key_path+".key", 'rb')
            priv_key = file.read()
            file.close()
            priv_key = RSA.importKey(priv_key) # set private key in mem

        except FileNotFoundError:
            # generate RSA key pair
            priv_key = RSA.generate(self.__encryption_size,Random.new().read)
            #? export keys to bytes
            priv_key_bytes = priv_key.exportKey()


            # create file and write to it key (bytes)
            with open(self.__key_path+".key", 'wb') as fp:
                fp.write(priv_key_bytes) # saves priv key to file @ self._key_path "ex.: ./key.key"
                fp.close()
            pass
        if priv_key is not None:
            self.__priv_key_RSA = priv_key
        return priv_key

    def _key_open_RSAPub(self):
        try:
            pub_key = None
            file = open(self.__key_path+".pub", 'rb')
            pub_key = file.read()
            file.close()
            pub_key = RSA.importKey(pub_key) # set public key in mem

        except FileNotFoundError:
            # generate RSA key pair
            self._key_open_RSAPair()
            pass
        if pub_key is not None:
            self.__pub_key_RSA = pub_key
        return self.__pub_key_RSA

    def _key_open_RSAPair(self):
        try:
            priv_key = None
            file = open(self.__key_path+".key", 'rb')
            priv_key = file.read()
            file.close()
            priv_key = RSA.importKey(priv_key) # set private key in mem

            file = open(self.__key_path+".pub", 'rb')
            pub_key = file.read()
            file.close()
            pub_key = RSA.importKey(pub_key) # set public key in mem

        except FileNotFoundError:
            # generate RSA key pair
            if priv_key is None:
                priv_key = RSA.generate(self.__encryption_size,Random.new().read)
            pub_key = priv_key.publickey()
            #? export keys to bytes
            priv_key_bytes = priv_key.exportKey()
            pub_key_bytes = pub_key.exportKey()

            # create file and write to it key (bytes)
            with open(self.__key_path+".key", 'wb') as fp:
                fp.write(priv_key_bytes) # saves priv key to file @ self._key_path "ex.: ./key.key"
                fp.close()
            with open(self.__key_path+".pub", 'wb') as fp:
                fp.write(pub_key_bytes) #! OVERWRITES ANY PUB KEY WITH SAME FILE NAME "ex.: ./key"
                fp.close()
            pass

        self.__priv_key_RSA = priv_key
        self.__pub_key_RSA = pub_key
        return priv_key,pub_key
    
    def _encrypt_aes(self,message,private_key_aes): # output = C1
        message = self.__pad(message,self.__BLOCK_SIZE)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key_aes,AES.MODE_CBC,iv)
        return base64.b64encode(iv+cipher.encrypt(message))

    def _encrypt_rsa(self,private_key_aes,public_key_rsa): # output = C2
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
        # m_bytes = bytes(private_key_aes, 'utf-8') # convert to bytes from string
        # #? .encode('utf-8')
        # encoded = base64.b64encode(m_bytes) # encode bytes
        encoded = base64.b64encode(private_key_aes)
        #? encoded = m.encode()
        return public_key_rsa.encrypt(encoded,32) # encrypt

    def _decrypt_aes(self,c1,private_key_aes):
        c1 = base64.b64decode(c1)
        iv = c1[:16]
        cipher = AES.new(private_key_aes, AES.MODE_CBC, iv)
        return self.__unpad(cipher.decrypt(c1[16:]))

    def _decrypt_rsa(self,c2,private_key_rsa): # aka. priv key AES
        decrypted = private_key_rsa.decrypt(c2) # decrypted bytes
        return base64.b64decode(decrypted)
        # decoded = base64.b64decode(decrypted)# decoded bytes
        # #? decoded = decrypted.decode()
        # return decoded.decode('utf-8') # convert to string from bytes

    def _calc_blocks(self,input_len,block_size):
        modulo = input_len%block_size
        extra=0
        if modulo > 0:
            extra=1
            input_len-=modulo
        return int(input_len/block_size+extra)

    def _encrypt_rsa_only(self,data,public_key_rsa):
        if isinstance(data, str):
            data_bytes = bytes(data, 'utf-8')
        elif isinstance(data,bytes):
            data_bytes = data
        else:
            raise TypeError('Data for encryption has to be STRING UTF-8 or BYTES')
        enc_size_bytes=int(min(public_key_rsa.size()/8-42,245))
        blocks = self._calc_blocks(len(data_bytes),enc_size_bytes)
        output = bytes()
        for n in range(blocks):
            start = n*enc_size_bytes
            end = (n+1)*enc_size_bytes
            part = data_bytes[start:end]
            encoded_data = base64.b64encode(part)
            output += public_key_rsa.encrypt(encoded_data,32)[0]
        return output

    def _decrypt_rsa_only(self,data,private_key_rsa):
        if not isinstance(data,bytes):
            raise TypeError('Data for decryption has to be BYTES')
        dec_size_bytes=512
        if len(data) % dec_size_bytes != 0:
            raise ValueError('Encrypted data has to be in 512 bytes block size')
        decoded_data_bytes = bytes()
        for n in range(round(len(data)/dec_size_bytes)):
            start = n*dec_size_bytes
            end = (n+1)*dec_size_bytes
            part = data[start:end]
            decrypted = private_key_rsa.decrypt(part)
            decoded_data_bytes += base64.b64decode(decrypted)
        return decoded_data_bytes

    def encrypt_RSA(self):
        self._key_open_RSAPub()
        return self._encrypt_rsa_only(self.__message,self.__pub_key_RSA)

    def decrypt_RSA(self):
        self._key_open_RSAPriv()
        return self._decrypt_rsa_only(self.__message,self.__priv_key_RSA)

    def encrypt(self):
        self._key_open_RSAPub()
        self._key_open_AESPriv()
        self.__c1 = self._encrypt_aes(self.__message,self.__priv_key_AES)
        self.__c2 = self._encrypt_rsa(self.__priv_key_AES,self.__pub_key_RSA)
        return self.__c1,self.__c2

    def decrypt(self):
        self._key_open_RSAPriv()
        # self._key_open_AESPriv()
        try:
            self.__priv_key_AES = self._decrypt_rsa(self.__c2,self.__priv_key_RSA) # aka. priv key AES
        except:
            self.encrypt()
            self.__priv_key_AES = self._decrypt_rsa(self.__c2,self.__priv_key_RSA)
        decoded = self._decrypt_aes(self.__c1,self.__priv_key_AES) # message
        return decoded.decode('utf-8')

    def RSA_priv_key_size(self):
        self._key_open_RSAPriv()
        return self.__priv_key_RSA.size()

"""      
        # max_size_bytes = int((self.key_size()+1)/8-42)
        # encrypted = bytes()
        # if max_size_bytes < len(encoded):
        #     a = 0
        #     while(a+max_size_bytes<=len(encoded)):
        #         begin = a
        #         if (a+max_size_bytes < len(encoded)):
        #             end = a+max_size_bytes
        #         else:
        #             end = len(encoded)
        #         encrypted_data = self.__pub_key.encrypt(encoded[begin:end],32) # encrypt
        #         encrypted += encrypted_data[0]
        #         a+=max_size_bytes
        # else:


        # encrypt data ( decrypt-> decode -> data )
        # max_size_bytes = int((self.key_size()+1)/8-42)
        # decrypted = bytes()
        # if max_size_bytes < len(self.__message):
        #     a = 0
        #     while(a+max_size_bytes<=len(self.__message)):
        #         begin = a
        #         if (a+max_size_bytes < len(self.__message)):
        #             end = a+max_size_bytes
        #         else:
        #             end = len(self.__message)
        #         decrypted_data = self.__priv_key.decrypt(self.__message[begin:end]) # decrypt
        #         decrypted += decrypted_data
        #         a+=max_size_bytes
        # else:
"""