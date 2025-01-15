import socket
import threading

HOST = '127.0.0.1'
PORT = 21002

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                # This condition is no longer needed since we get the nickname before connecting
                continue
            else:
                print("\n" + message)  # Add a newline before displaying a new message
                print("You: ", end='')  # Prompt user input after each message
        except:
            print("An error occurred!")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input("")
        if message.lower() == "exit":
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))

def start_client():
    nickname = input("Enter your nickname: ")  # Prompt for nickname before connecting
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Send the nickname to the server immediately after connecting
    client_socket.send(nickname.encode('utf-8'))

    thread_receive = threading.Thread(target=receive_messages, args=(client_socket,))
    thread_receive.start()

    thread_send = threading.Thread(target=send_messages, args=(client_socket,))
    thread_send.start()

if __name__ == "__main__":
    start_client()
