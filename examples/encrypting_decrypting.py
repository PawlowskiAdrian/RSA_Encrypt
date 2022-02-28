import v2.encryption_module as em

secret_message: str = "top_secret message as a string"

"""
00001-key.aes -> aes priv key
00001-key.key -> rsa priv key
00001-key.pub -> rsa pub key

keys can be auto generated if none are put into this folder.
"""

c1, c2 = em.encrypt_hybrid(secret_message) # message at c1 + aes_priv at c2 (encrypted aes with rsa)
d1 = em.encrypt_aes(secret_message)

print(c1,c2)
print(d1)

m1 = em.decrypt_hybrid(c1,c2) # rsa/aes, requires rsa priv
m2 = em.decrypt_aes(d1) # aes, requires aes priv

print(m1)
print(m2)