# RSA_Encrypt
Python Class for handling message encryption with RSA,AES key pairs

## Use case
AES encryption is fast and does not require lot of computional power and is higly secure.
Unfortunatelly AES has only private key and sending it with any channel is not secure.
RSA can help to encrypt AES priv key with secure maner. We only need RSA pub of recipient.
Recipient will then decrypt AES priv with his RSA priv key.

# Future improvements
- password generator

# How to install?
Download repo to your computer
`git clone https://github.com/PawlowskiAdrian/RSA_Encrypt.git`

Copy/Move `v2/*.py` to directory of your wish.

Install requirements from `v2/requirements.txt` with `pip3 install -r requitements.txt`

## OS env for AES (will be secured with PBKDF2) - optional
```
AES_PRIVATE_KEY_PASSWORD=verystrongentrophypasswordhere
AES_SALT=thisissaltANDisusedforPBKDF2
```
