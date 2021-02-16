# RSA_Encrypt
Python Class for handling message encryption with RSA,AES key pairs

## Use case
Imagine you have top secret message you would like to encrypt with top level security.

I have writen script which I use for handling sensitive files over internet `SECURE.py`
To prepare, edit first few variables for your needs:
```
KEY_PATH = 00002-key # Type filename if you are DECRYPTING with your PRIVATE KEY
# KEY_PATH = None # use None if you are Encrypting and will use NEW keys
SAVE_PATH='DELIVERY'
```

1) you have to send over internet (secure connection prefered) your RSA PUBLIC key to someone who will ENCRYPT data.

If you RECEIVED PUBLIC RSA KEY, you have to modify `KEY_PATH` to USE this key.
example:
```
# got 00001-key.pub -> KEY_PATH = 00001-key
KEY_PATH = 00001-key
SAVE_PATH='DELIVERY'
```

2) send data from `DELIVERY` folder to host with PRIVATE RSA key.
3) you were encrypting data with your automaticly generated keys, so you can leave:
```
KEY_PATH = None
SAVE_PATH='DELIVERY'
```
4) create Encryptor object on host `secure_handler = ENC(top_secret_data)`
5) decrypt data using `output = secure_handler.decrypt()`


# Future improvements
- use private variables with `__variable` to secure Encryptor module
- password generator

# How to install?
Download repo to your computer
`git clone https://github.com/PawlowskiAdrian/RSA_Encrypt.git`

Copy/Move `RsaEncrypt.py` to directory of your wish.

Install requirements from `requirements.txt` with `pip3 install -r requitements.txt`
# Functions and usage of `Encryptor CLASS`

## Create file with password for AES (will be secured with PBKDF2) - optional
`vi .aes_psw` and put there:
```
AES_PRIVATE_KEY_PASSWORD=verystrongentrophypasswordhere
AES_SALT=thisissaltANDisusedforPBKDF2
```

## In YOUR Python project import class:
`from RsaEncrypt import Encryptor as ENC`

## Write desired messages / Input DATA, as a STRING:
`top_secret_data = 'Secret message or DATA'`
* data will be converted to bytes using UTF-8 standard during encryption process

### Extra step (not required)
Create your own RSA key pairs

```
from Crypto.PublicKey import RSA # to generate RSA keys, work with enc/dec
from Crypto import Random # to generate random numbers

priv_key = RSA.generate(self._encryption_size,Random.new().read)
pub_key = priv_key.publickey()

priv_key_bytes = priv_key.exportKey() # here is your priv key as a string of bytes
pub_key_bytes = pub_key.exportKey() # here is your pub key as a string of bytes
```

Save `priv_key_bytes` and `pub_key_bytes` to files:
`priv_key_bytes` to `key.key`
`pub_key_bytes` to `key.pub`

## Create Encryptor object:
Option 1) - without your keys, with automaticly generated key pair at 4096 bytes size for RSA and AES private key with entrophy level above 260 bits. Note: You can tweek creation for AES private key AND RSA key pair.
`secure_handler = ENC(top_secret_data)`

Option 2) - with YOUR keys
- Required for ENCRYPTION: `00001-key.pub` [RSA PUB] & `00001-key.aes` [AES PRIV]
- Required for DECRYPTION: `00001-key.aes` [AES PRIV] OR `c2.bin` [ENCRYPTED AES PRIV] & `00001-key.key` [RSA PRIV]
* `c2.bin` is output file during ENCRYPTION process. It is secured AES private key with RSA public key.
```
key_path='~/Documents/00001-key'
secure_handler = ENC(top_secret_data,key_path=key_path)
```

Option 3) - WITHOUT your keys and with modified encryption size
* Size min. is 256 * 4 = 1024. Your INPUT is INT, which is minimum 4
`secure_handler = ENC(top_secret_data,encryption_size_multiplier=32)`
The bigger multiplier, the longer key generation and encryption/decryption will take place.
You also have limit for securing AES key with RSA, if RSA is too short and AES is too long.
More information in comment in `RsaEncrypt.py`

## Functions of Encryptor object for encryption/decryption
* You have created class object `secure_handler`

You are able to:
- find available name for key path with: `secure_handler._find_key_path()`
- extract keys from files to memory *: 
```
aes_priv_key = secure_handler._key_open_AESPriv()
rsa_priv_key = secure_handler._key_open_RSAPriv()
rsa_pub_key = secure_handler._key_open_RSAPub()
(rsa_priv_key, rsa_pub_key) = secure_handler._key_open_RSAPair()
```
* those functions CAN create keys if Requested INPUT is not available
- encrypt/decrypt data in `top_secret_data` with `secure_handler.encrypt()`, `secure_handler.decrypt()`
* requirements for DECRYPTION: 
1) Data in `top_secret_data` has to be STRING DATA (output from ENCRYPTION).
2) Folder with running script needs to have `data.bin` AND `c2.bin` (or SAME AES PRIV key instead of `c2.bin`)
Route for encryption:
DATA -> ENCODE -> ENCRYPT -> ENCRYPTED DATA

Route for decryption:
ENCRYPTED DATA -> DECRYPT -> DECODE -> DATA

### Encryption example:
* message need to be tuple type and include string
* requires public key but it automatically generate your key pair without setting correct key_path (.key and .pub)
- good key_path = `~/your_key` -> requires `your_key.pub` in same folder for encryption
```
from RsaEncrypt import Encryptor as ENC

message = 'SECRET'
secure_handler = ENC(message,encryption_size_multiplier=4)
encrypted_data = secure_handler.encrypt()
```

For this example output with keys `00001-key.key`, `00001-key.pub` and `00001-key.aes` is:
```
>>> from RsaEncrypt import Encryptor as ENC
>>> message = 'SECRET'
>>> secure_handler = ENC(message,encryption_size_multiplier=4)
>>> encrypted_data = secure_handler.encrypt()
>>> encrypted_data
(b'lWLKeN9e9DqTEZBkWUjQitMJ9fF2InVfc61/V055F8A=', (b"j/\x8b1qj\x024\\C\xe8\xa6.\xfc\xc3\xe6\xdb\xb7\x96\x01Y\x9e\xe7\x0c\xc5\xa6\x16\x92N\xa6=\x1ft\x82U|JD\x96*\r\xae\xc9\xe9\xa1\x9bF\x15\xc71mp\x02@B\xeeR\xf9\x12\xe0M\x14\x14o\x1ed\xa8,oe\xb5\xc9\xbc\xbf/\xd7\xc0A\x95\x91S\xda\x00\xa2RC\xa0\xb1E\x97\x89\xee\xd9\x8a-\xb3\x07\xfc\xaa\x7f'\xff\r\x87\x81\x1f~\x80\xad?X\xda6\x8f\xb3S\x19!\t\x9fD\xbbQR\xa5r\xe6\x17",))
>>> 
```

### Decryption example:
* !!! requires RSA private key `*.key` !!!
```
from RsaEncrypt import Encryptor as ENC

message = <output from encryption>[1][0]
rsa_handler = ENC(message,key_path='00001-key')
decrypted_data = rsa_handler.decrypt()
```

Output will be string. For this example output with my keys `00001-key.key`, `00001-key.pub` and `00001-key.aes` is:
```
>>> message = <output from encryption>[1][0]
>>> rsa_handler = ENC(message,key_path='00001-key')
>>> decrypted_data = rsa_handler.decrypt()
>>> decrypted_data
'SECRET'
>>>
```