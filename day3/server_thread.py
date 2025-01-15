import socket
import threading

HOST = '127.0.0.1'
PORT = 21002

def handle_client_connection(client_socket):
    print("Client connected:", client_socket.getpeername())
    try:
        while True:
            message = input("Enter a message to send to the client (or type 'exit' to disconnect): ")
            if message.lower() == 'exit':
                break
            client_socket.send((message + "\n").encode())
    except Exception as e:
        print("Connection error:", e)
    finally:
        client_socket.close()
        print("Client disconnected:", client_socket.getpeername())

def receive_messages(server_socket):
    while True:
        message_received = ""
        while True:
            data = server_socket.recv(1024)
            if data:
                print('Received data chunk from client:', repr(data))
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

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
            client_thread.start()
            server_thread = threading.Thread(target=receive_messages, args=(client_socket,)) 
            server_thread.start()

if __name__ == "__main__":
    start_server()
