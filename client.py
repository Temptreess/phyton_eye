import socket
import webbrowser
from PIL import ImageGrab
import io
import struct
import time

def take_screenshot():
    screenshot = ImageGrab.grab()
    image_bytes = io.BytesIO()
    screenshot.save(image_bytes, format='PNG')
    return image_bytes.getvalue()

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to the server {host}:{port}")

    try:
        while True:
            # Get the first message from the server
            data = client_socket.recv(4096).decode()
            if data == "quit":
                print("Server terminated the connection.")
                break

            if data == "link":
                url = client_socket.recv(4096).decode()
                webbrowser.open(url)
                time.sleep(5)
                # Take a screenshot
                screenshot_bytes = take_screenshot()

                # Get the screenshot data length in bytes
                screenshot_length = len(screenshot_bytes)
                # Send the screenshot data length to the server
                client_socket.sendall(struct.pack('!I', screenshot_length))

                # Send the screenshot data to the server
                client_socket.sendall(screenshot_bytes)

            elif data == "text":
                file_name = str(client_socket.recv(4096).decode() + ".txt")  # Set your desired file name here
                file_text = str(client_socket.recv(4096).decode())

                # Open the file for writing (or create a new one if it doesn't exist)
                with open(file_name, 'w') as file:
                    file.write(str(file_text))

                back_send = str("File_name: " + file_name + " File_text: " + file_text)
                client_socket.sendall(back_send.encode())

            else:
                client_socket.sendall("Error".encode())

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Local host
    PORT = 12345       # Port number
    start_client(HOST, PORT)
