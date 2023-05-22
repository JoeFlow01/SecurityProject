import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def decrypt_session_key(encrypted_session_key, master_key):
    cipher = Cipher(algorithms.AES(master_key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    session_key = decryptor.update(encrypted_session_key) + decryptor.finalize()
    return session_key


def start_client(host, port):
    with open("../TextFiles/SenderMasterKey.txt", 'rb') as infile:
        SenderMasterKey = infile.read()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    client_socket.send("Request Session Key".encode('utf-8'))
    encrypted_session_key_sender = client_socket.recv(1024)
    encrypted_session_key_receiver = client_socket.recv(1024)

    session_key_sender = decrypt_session_key(encrypted_session_key_sender, SenderMasterKey)
    print("Session key: ",session_key_sender)

    client_socket.close()
    print("Connection closed")
    return session_key_sender,encrypted_session_key_receiver


if __name__ == '__main__':
    host = "localhost"
    port = 65535
    start_client("localhost", 65535)
