import socket
import threading

HOST = '10.237.21.42'
PORT = 12345

def send_message_function(client_socket):
    while True:
        message = input("Enter a message: ")
        client_socket.send((message + "\n").encode())

def receive_messages(client_socket):
    while True:
        message_received = ""
        while True:
            data = client_socket.recv(1024)
            if data:
                print('Received data chunk from server:', repr(data))
                message_received += data.decode()
                if message_received.endswith("\n"):
                    print("End of message received")
                    break
            else:
                print("Connection lost!")
                return
        if not message_received:
            break
        print("Received message:", message_received)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server")

    send_thread = threading.Thread(target=send_message_function, args=(s,))
    send_thread.start()

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

print("Client finished")
