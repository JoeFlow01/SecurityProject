from aes import *
from SenderClient import DecryptKey

with open("RecieverEncryptedkey.txt", "rb") as file:
    RecieverEncrypted = file.read()
    print("@reciever(RecieverEncrypted) ",RecieverEncrypted)

with open("ReciverPrivateKey.txt", "r") as file:
    ReciverPrivateKey = file.read()
    print("@reciever(ReciverPrivateKey) ", ReciverPrivateKey)

key=DecryptKey(RecieverEncrypted,ReciverPrivateKey)

decrypt_file(key, 'EncryptedMessage.txt', 'DecryptedMessage.txt')

