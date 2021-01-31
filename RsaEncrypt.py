import os # to work with path on OS
from Crypto.PublicKey import RSA # to generate RSA keys, work with enc/dec
from Crypto import Random # to generate random numbers
import base64 # to work with bytes

# By default RSA requires min. 256*4 size, so any value set below 4 will be set to 4 by default

class RSA_Encrypt:
    def __init__(self,messages=(),key_path=None,encryption_size_multiplier=None):
        try:
            self._priv_key=None
            self._pub_key=None
            if encryption_size_multiplier is not None: # encryption key size <-- force to create NEW key pairs
                self._encryption_size=256*min(int(encryption_size_multiplier),4)
                self._key_path = self._find_key_path()
            else:
                if key_path is not None: # specified custom key, if not -> create new key pair with default values
                    self._key_path = key_path # holds path to key file
                else:
                    self._key_path = self._find_key_path()
                    self._encryption_size=256*16 # this will be executed only if key_path=None AND encryption_size=None
            self._messages=messages # list of messages to encrypt/decrypt
        except:
            print('Error occured!\n \
                messages = args tuple\n \
                key_path = not required, full path to .key & .pub file (same name required)\n \
                encryption_size_multiplier = integer >= 4\n')

    def _find_key_path(self):
        path_finder=None
        increment=1
        while(path_finder==None):
            try:
                path_finder = "%s-key.key" %(str(increment).zfill(5))
                file = open(path_finder, 'rb') # exception or NOT
                file.close() # finds first not set filename for .key
                #!!! IT WILL OVERWRITE PUBLIC KEY FOR THE SAME FILE NAME !!!
            except FileNotFoundError:
                increment+=1 
                continue
        return path_finder

    def _key_open(self):
        # get priv key for encryption
        try:
            file = open(self._key_path, 'rb')
            priv_key = file.read()
            file.close()
            priv_key = RSA.importKey(priv_key) # set private key in mem

            file = open(self._key_path[:len(self._key_path)-4]+".pub", 'rb')
            pub_key = file.read()
            file.close()
            pub_key = RSA.importKey(pub_key) # set public key in mem

        except FileNotFoundError:
            # generate key
            priv_key = RSA.generate(self._encryption_size,Random.new().read)
            pub_key = priv_key.publickey()

            #? export keys to bytes
            priv_key_bytes = priv_key.exportKey()
            pub_key_bytes = pub_key.exportKey()
            # create file and write to it key (bytes)
            with open(self._key_path, 'wb') as fp:
                fp.write(priv_key_bytes) # saves priv key to file @ self._key_path "ex.: ./key.key"
                fp.close()
            with open(self._key_path[:len(self._key_path)-4]+".pub", 'wb') as fp:
                fp.write(pub_key_bytes) #! OVERWRITES ANY PUB KEY WITH SAME FILE NAME "ex.: ./key"
                fp.close()
            pass
        return priv_key, pub_key

    def encrypt(self):
        self._priv_key, self._pub_key = self._key_open()
        # encrypt data ( data -> encode -> encrypt )
        encrypted_output = []
        for m in self._messages: # m = data (string)
            m_bytes = bytes(m, 'utf-8') # convert to bytes from string
            #? .encode('utf-8')
            encoded = base64.b64encode(m_bytes) # encode bytes
            #? encoded = m.encode()
            encrypted = self._pub_key.encrypt(encoded,32) # encrypt
            encrypted_output.append(encrypted) # put on stack
        return tuple(encrypted_output)

    def decrypt(self):
        self._priv_key, self._pub_key = self._key_open()
        # encrypt data ( decrypt-> decode -> data )
        decrypted_output = []
        for m in self._messages: # m = encrypted (bytes)
            decrypted = self._priv_key.decrypt(m) # decrypted bytes
            decoded = base64.b64decode(decrypted)# decoded bytes
            #? decoded = decrypted.decode()
            decoded_str = decoded.decode('utf-8') # convert to string from bytes
            decrypted_output.append(decoded_str) # put on stack
        return tuple(decrypted_output)