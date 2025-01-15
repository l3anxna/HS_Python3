import socket
import select
import sys

HOST = "127.0.0.1"
PORT = 21002

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server")

        while True:
            print("Enter a message(or 'exit' to quit): ")
            readable, _, _ = select.select([s, sys.stdin], [], [])

            for r in readable:
                if r == s:
                    data = s.recv(1024)
                    if data:
                        print("Received from server:", data.decode().strip())
                    else:
                        print("Connection closed by server.")
                        exit(0)

                elif r == sys.stdin:
                    message = input()
                    if message.lower() == "exit":
                        print("Exiting client.")
                        s.send((message + "\n").encode())
                        exit(0)
                    s.send((message + "\n").encode())

except ConnectionRefusedError:
    print("Could not connect to the server. Ensure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")

print("Client finished")
