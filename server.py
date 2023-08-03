import socket
import threading
import struct

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def handle_client(client_socket, client_address):
    try:
        while True:
            ques = ("What do you want to do?\n"
                    "1-Open link\n"
                    "2-Write something to file\n"
                    "3-Quit\n")
            print(ques)
            answer = input("\nWhat do you want to do? (type the number)")

            if answer == "1":
                type = "link"
                data_to_send1 = input("Link: ")
                client_socket.sendall(type.encode())
                client_socket.sendall(data_to_send1.encode())

                # Get the screenshot data length from the client
                length_data = recvall(client_socket, 4)
                screenshot_length = struct.unpack('!I', length_data)[0]

                # Get the screenshot data from the client
                screenshot_data = recvall(client_socket, screenshot_length)

                with open(f"screenshot_{client_address[0]}_{client_address[1]}.png", "wb") as f:
                    f.write(screenshot_data)
                print(f"Screenshot saved from the client {client_address[0]}:{client_address[1]}")

            elif answer == "2":
                type = "text"
                client_socket.sendall(type.encode())
                data_to_send1 = input("Name: ")
                client_socket.sendall(data_to_send1.encode())
                data_to_send2 = input("Text: ")
                client_socket.sendall(data_to_send2.encode())
                data = client_socket.recv(4096).decode()
                print("Data from the client:", data)

            elif answer == "3":
                print("Client terminated the connection.")
                break

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started. Waiting for connections on {host}:{port}...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address[0]}:{client_address[1]}")

            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()

    finally:
        server_socket.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Local host
    PORT = 12345       # Port number
    start_server(HOST, PORT)
