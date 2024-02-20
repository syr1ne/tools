#!/usr/bin/env python3

from sys import argv
from cryptography.fernet import Fernet
import base64, hashlib
from getpass import getpass

def gen_fernet_key(masterpass:bytes) -> bytes:
    assert isinstance(masterpass, bytes)
    hlib = hashlib.md5()
    hlib.update(masterpass)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def master():
    masterpass = getpass("masterpass: ")
    key = gen_fernet_key(masterpass.encode('utf-8'))
    global fernet
    fernet = Fernet(key)

def encrypt():
    with open(file, 'r') as unencrypted_file:
        unencrypted_file.seek(0)
        data = unencrypted_file.read()
        cipher = fernet.encrypt(data.encode('utf-8'))
        with open("encrypted.data", 'w') as output_file:
            output_file.seek(0)
            output_file.write(str(cipher.decode('utf-8')))


def decrypt():
    with open(file, 'r') as encrypted_file:
        encrypted_file.seek(0)
        cipher = encrypted_file.read()
        try:
            data = fernet.decrypt(cipher.encode('utf-8')).decode('utf-8')
        except:
            print("incorrect master password")
            exit()
        with open("decrypted.data", 'w') as output_file:
            output_file.seek(0)
            output_file.write(data)

file = argv[2]
if argv[1] == "e":
    master()
    encrypt()
elif argv[1] == "d":
    master()
    decrypt()
else:
    print("wrong input")
    exit()
