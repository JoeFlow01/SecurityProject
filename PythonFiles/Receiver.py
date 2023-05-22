from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from aes import *

def decrypt_session_key(encrypted_session_key, master_key):
    cipher = Cipher(algorithms.AES(master_key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    session_key = decryptor.update(encrypted_session_key) + decryptor.finalize()
    return session_key

with open("../TextFiles/ReceiverMasterKey.txt", 'rb') as infile:
    ReceiverMasterKey = infile.read()


with open("../TextFiles/ReceiverEncryptedKey.txt", 'rb') as infile:
    ReceiverEncryptedKey = infile.read()



Sessionkey = decrypt_session_key(ReceiverEncryptedKey,ReceiverMasterKey)


decrypt_file(Sessionkey,"../TextFiles/EncryptedMessage.txt","../TextFiles/DecryptedMessage.txt")
