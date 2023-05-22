import socket
from Cryptodome.Random import get_random_bytes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt_session_key(session_key, master_key):
    cipher = Cipher(algorithms.AES(master_key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_session_key = encryptor.update(session_key) + encryptor.finalize()
    return encrypted_session_key





def start_server(host, port):
    with open("../TextFiles/SenderMasterKey.txt", 'rb') as infile:
        SenderMasterKey = infile.read()
    with open("../TextFiles/ReceiverMasterKey.txt", 'rb') as infile:
        ReceiverMasterKey = infile.read()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(4)
    print(f"Server started on {host}:{port}")

    while True:
        SessionKey = get_random_bytes(16)
        print("Session key: ",SessionKey)
        client_socket, client_address = server_socket.accept()
        print(f"Connection established from {client_address[0]}:{client_address[1]}")
        request = client_socket.recv(1024).decode('utf-8')
        SessionKeyEncryptedBySenderMasterKey = encrypt_session_key(SessionKey, SenderMasterKey)
        SessionKeyEncryptedByReceiverMasterKey = encrypt_session_key(SessionKey, ReceiverMasterKey)
        client_socket.send(SessionKeyEncryptedBySenderMasterKey)
        client_socket.sendall(SessionKeyEncryptedByReceiverMasterKey)
        client_socket.close()
        print(f"Connection closed from {client_address[0]}:{client_address[1]}")

if __name__ == '__main__':
    host = "localhost"
    port = 65535
    start_server(host, port)
