from RsaEncrypt import Encryptor as enc
from dotenv import load_dotenv
from signal import signal, SIGINT
import os
import sys

# KEY_PATH='00002-key' # or set to None
KEY_PATH = None
SAVE_PATH_HYBRID='DELIVERY_RSA-AES'
SAVE_PATH='DELIVERY_RSA'

INPUT_DATA=None
try:
    if len(sys.stdin)>0:
        for line in sys.stdin:
            INPUT_DATA = str(line[:1])
except:
    pass

def encryption():
    file = open(file_list[0], 'r')
    data_to_save = file.read()
    file.close()
    # PUT DATA in SECURE MODULE and ENCRYPT
    a = enc(message=data_to_save,key_path=KEY_PATH)
    bytes_like_object = a.encrypt()
    # bytes_like_object[0] # c1 (big binary data)
    # bytes_like_object[1] # c2 (small and tuple object)
    output_file = os.path.join(os.getcwd(),SAVE_PATH_HYBRID, file_list[0]+'.bin')
    with open(output_file, 'wb') as fp:
        fp.write(bytes_like_object[0])
        fp.close()
    output_file = os.path.join(os.getcwd(),SAVE_PATH_HYBRID, 'c2.bin')
    with open(output_file, 'wb') as fp:
        fp.write(bytes_like_object[1][0])
        fp.close()
        print('Created:','c2.bin')

    for f in file_list[1:]:
        # READ DATA TO SECURE
        file = open(f, 'r')
        data_to_save = file.read()
        file.close()
        # PUT DATA in SECURE MODULE and ENCRYPT
        a = enc(message=data_to_save,key_path=KEY_PATH)
        bytes_like_object = a.encrypt()
        # SAVE ENCRYPTED DATA TO .BIN
        output_file = os.path.join(os.getcwd(),SAVE_PATH_HYBRID, f+'.bin')
        with open(output_file, 'wb') as fp:
            fp.write(bytes_like_object[0])
            fp.close()
            print('Created:',f+'.bin')
def encryption_rsa():
    for f in file_list:
        # READ DATA TO SECURE
        file = open(f, 'r')
        data_to_save = file.read()
        file.close()
        # PUT DATA in SECURE MODULE and ENCRYPT
        a = enc(message=data_to_save,key_path=KEY_PATH)
        bytes_like_object = a.encrypt_RSA()
        # SAVE ENCRYPTED DATA TO .BIN
        output_file = os.path.join(os.getcwd(),SAVE_PATH, f+'.bin')
        with open(output_file, 'wb') as fp:
            fp.write(bytes_like_object)
            fp.close()
            print('Created:',f+'.bin')

###### DECRYPTION
def decryption():
    with open('c2.bin', 'rb') as fp:
        c2 = fp.read()
        fp.close()

    for f in file_list:
        # READ DATA TO SECURE
        file = open(f+'.bin', 'rb')
        data_to_save = file.read()
        file.close()
        # PUT DATA in SECURE MODULE and DECRYPT
        a = enc(c1=data_to_save,c2=c2,key_path=KEY_PATH)
        string_object = a.decrypt()
        # SAVE DECRYPTED DATA TO .py
        output_file = os.path.join(os.getcwd(),SAVE_PATH_HYBRID, f)
        with open(output_file, 'w') as fp:
            fp.write(string_object)
            fp.close()
            print('Created:',f)
def decryption_rsa():
    for f in file_list:
        # READ DATA TO SECURE
        file = open(f+'.bin', 'rb')
        data_to_save = file.read()
        file.close()
        # PUT DATA in SECURE MODULE and DECRYPT
        a = enc(message=data_to_save,key_path=KEY_PATH)
        string_object = a.decrypt_RSA().decode()
        # SAVE DECRYPTED DATA TO .py
        output_file = os.path.join(os.getcwd(),SAVE_PATH, f)
        with open(output_file, 'w') as fp:
            fp.write(string_object)
            fp.close()
            print('Created:',f)

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

# CTRL+C function
signal(SIGINT, handler)

if KEY_PATH is not None:
    print('Using imported keys:', KEY_PATH)

file_list = ('id_ed25519_MS','id_ed25519_MS.pub')

print('Mode: 1 -> encryption hybrid\n\
Mode: 2 -> decryption hybrid\n\
Mode: 3 -> encryption RSA\n\
Mode: 4 -> decryption RSA')
mode_nr = 0

while mode_nr != '1' and mode_nr != '2' and mode_nr != '3' and mode_nr != '4':
    if INPUT_DATA is not None:
        mode_nr = INPUT_DATA
    else:
        mode_nr = input('Select MODE:')
    continue

print('OUTPUT files are put in directory:',SAVE_PATH)
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
    print('OUTPUT folder not existing. Creating folder:',SAVE_PATH)

if not os.path.exists(SAVE_PATH_HYBRID):
    os.makedirs(SAVE_PATH_HYBRID)
    print('OUTPUT folder not existing. Creating folder:',SAVE_PATH_HYBRID)

if mode_nr == '1' :
    # CREATE OUTPUT DIRECTORY
    encryption()
    print('Files encrypted. Saved in:',SAVE_PATH_HYBRID)
elif mode_nr == '2' : 
    decryption()
    print('Files decrypted. Saved in:',SAVE_PATH_HYBRID)
elif mode_nr == '3' : 
    encryption_rsa()
    print('Files encrypted. Saved in:',SAVE_PATH)
elif mode_nr == '4' : 
    decryption_rsa()
    print('Files decrypted. Saved in:',SAVE_PATH)