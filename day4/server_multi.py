import socket
import threading

HOST = '127.0.0.1'
PORT = 21002

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(f'other client: {message}')
            else:
                index = clients.index(client_socket)
                clients.remove(client_socket)
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat.'.encode('utf-8'))
                nicknames.remove(nickname)
                break
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat.'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive_connections(server_socket):
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connected with {str(address)}")
        
        client_socket.send('NICKNAME'.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client_socket)

        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined the chat.".encode('utf-8'))
        client_socket.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    receive_connections(server_socket)

if __name__ == "__main__":
    start_server()
