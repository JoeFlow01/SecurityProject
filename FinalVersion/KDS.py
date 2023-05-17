import socket
import secrets
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes


def EncryptKey(key, public_keyStr):
    public_key=RSA.import_key(public_keyStr)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher.encrypt(key)
    return encrypted_key



def start_server(host, port):
    ServerDataBaseFile = 'ServerDataBase.txt'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(4)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established from {client_address[0]}:{client_address[1]}")
        key = get_random_bytes(16)
        print("key From Server : ",key)
        UsersString = client_socket.recv(2048).decode('utf-8')
        users=UsersString.split(",")
        with open(ServerDataBaseFile, "r") as file:
            string = file.read()
            list = string.split(",")

            for i in range(len(list)):
                if list[i] == users[0]:
                    print("Sender",list[i])
                    StrPublicKeySender=list[i + 1]
                    print("key",StrPublicKeySender)


        with open(ServerDataBaseFile, "r") as file:
            string = file.read()
            list = string.split(",")
            for i in range(len(list)):
                if list[i] == users[1]:
                    print("Reciver", list[i])
                    StrPublicKeyReciver=list[i + 1]
                    print("key", StrPublicKeyReciver)



        SenderEncryptedKey=EncryptKey(key,StrPublicKeySender)
        RecieverEncryptedKey=EncryptKey(key,StrPublicKeyReciver)
        client_socket.sendall(SenderEncryptedKey)
        client_socket.sendall(RecieverEncryptedKey)
        client_socket.close()

        print(f"Connection closed from {client_address[0]}:{client_address[1]}")

if __name__ == '__main__':
    host = "localhost"
    port = 65535
    start_server(host, port)
