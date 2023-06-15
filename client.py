import socket
from my_functions import *


def client_program():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    server_public_key = client_socket.recv(1024).decode()
    server_e, server_n, p, q = map(int, server_public_key.split(','))

    e, d = generate_keys(p, q)
    n = p * q

    print(f"Client public key: ({e}, {n})")

    print(f"Server public key: ({server_e}, {server_n})")

    client_socket.sendall(f"{e},{n}".encode())

    while True:
        message = input("Client: ")
        time_for_encryption = send_encrypted_message(
            client_socket, message, server_e, n)

        if message.lower() == "bye":
            break

        reply, time_for_decryption = receive_decrypted_message(
            client_socket, d, n)
        print(f"Server: {reply}")

    client_socket.close()
    # print(f"time for encryption:{time_for_encryption}")
    # print(f"time for decryption:{time_for_decryption}")


if __name__ == '__main__':
    client_program()
