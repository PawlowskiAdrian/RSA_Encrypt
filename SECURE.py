from RsaEncrypt import Encryptor as enc
from dotenv import load_dotenv
from signal import signal, SIGINT
import os

# KEY_PATH='00002-key' # or set to None
KEY_PATH = None
SAVE_PATH='DELIVERY'

def encryption():
    file = open(file_list[0], 'r')
    data_to_save = file.read()
    file.close()
    # PUT DATA in SECURE MODULE and ENCRYPT
    a = enc(message=data_to_save,key_path=KEY_PATH)
    bytes_like_object = a.encrypt()
    # bytes_like_object[0] # c1 (big binary data)
    # bytes_like_object[1] # c2 (small and tuple object)
    output_file = os.path.join(os.getcwd(),SAVE_PATH, file_list[0]+'.bin')
    with open(output_file, 'wb') as fp:
        fp.write(bytes_like_object[0])
        fp.close()
    output_file = os.path.join(os.getcwd(),SAVE_PATH, 'c2.bin')
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
        output_file = os.path.join(os.getcwd(),SAVE_PATH, f+'.bin')
        with open(output_file, 'wb') as fp:
            fp.write(bytes_like_object[0])
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

file_list = ('secret.py','.env')

print('Mode: 1 -> encryption()\n\
Mode: 2 -> decryption()')
mode_nr = 0
while mode_nr != '1' and mode_nr != '2':
    mode_nr = input('Select MODE:')
    continue

print('OUTPUT files are put in directory:',SAVE_PATH)
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
    print('OUTPUT folder not existing. Creating folder:',SAVE_PATH)

if mode_nr == '1' :
    # CREATE OUTPUT DIRECTORY
    encryption()
    print('Files encrypted. Saved in:',SAVE_PATH)
elif mode_nr == '2' : 
    decryption()
    print('Files decrypted. Saved in:',SAVE_PATH)