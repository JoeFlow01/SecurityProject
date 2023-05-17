import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def DecryptKey(encrypted_key, private_keyStr):
    private_key = RSA.import_key(private_keyStr)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_key = cipher.decrypt(encrypted_key)
    return decrypted_key



def start_client(host, port,SenderEmail,RecipientEmail):
    with open("SenderPrivateKey.txt", "r") as file:
        SenderPrivateStr = file.read()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    Users = SenderEmail + "," + RecipientEmail

    client_socket.sendall(Users.encode('utf-8'))
    SenderEncryptedkey = client_socket.recv(2048)
    print(f"Received from server  Senderkey: {SenderEncryptedkey}")
    RecieverEncryptedkey = client_socket.recv(2048)
    print(f"Received from server  Reciverkey: {RecieverEncryptedkey}")
    key=DecryptKey(SenderEncryptedkey,SenderPrivateStr)
    print(key)
    client_socket.close()
    print("Connection closed")
    return key,RecieverEncryptedkey


