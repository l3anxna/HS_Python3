import socket

HOST = "0.0.0.0"
PORT = 21002

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
except OSError as msg:
    print(f"Error creating socket: {msg}")
    exit(1)

try:
    s.bind((HOST, PORT))
    s.listen()
    print("Socket bound and listening")
except OSError:
    print("Error binding/listening!")
    s.close()
    exit(1)

conn, addr = s.accept()
with conn:
    print("Connection accepted from ", addr)

    while True:
        message_received = ""
        while True:
            data = conn.recv(1024)
            if data:
                print("Received data chunk from client: ", repr(data))
                message_received += data.decode()
                if message_received.endswith("\n"):
                    break
            else:
                print("Connection lost!")
                break

        if message_received:
            print("Received message: ", message_received.strip())
            response_message = "Server summarized: " + message_received[:10] + "\n"
            conn.send(response_message.encode())

            message_to_client = input("Enter a message to send to the client (or 'exit' to quit): ")
            if message_to_client.lower() == 'exit':
                break
            conn.send((message_to_client + "\n").encode())
        else:
            break

s.close()
print("Server finished")
