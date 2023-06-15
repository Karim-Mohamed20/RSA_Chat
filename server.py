import socket
from my_functions import *


def server_program(p, q):
    host = '127.0.0.1'
    port = 12345

    e, d = generate_keys(p, q)
    n = p * q
    print(f"Server public key: ({e}, {n})")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Waiting for client connection...")
    conn, address = server_socket.accept()
    print(f"Connection from {address}")

    conn.sendall(f"{e},{n},{p},{q}".encode())

    client_public_key = conn.recv(1024).decode()
    client_e, client_n = map(int, client_public_key.split(','))

    print(f"Client public key: ({client_e}, {client_n})")

    while True:
        message, time_for_decryption = receive_decrypted_message(conn, d, n)
        print(f"Client: {message}")

        if message.lower() == "bye":
            break

        reply = input("Server: ")
        time_for_encryption = send_encrypted_message(conn, reply, client_e, n)

    conn.close()
    # print(f"time for encryption:{time_for_encryption}")
    # print(f"time for decryption:{time_for_decryption}")


if __name__ == '__main__':
    # 31177 && 31193
    prime_1 = generate_random_prime(16)
    prime_2 = generate_random_prime(16)
    server_program(prime_1, prime_2)
