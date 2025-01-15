import socket

HOST = "127.0.0.1"
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"GET / HTTP/1.0\r\nHost: test.net\r\n\r\n")
    data = s.recv(1024)
print("Received", repr(data))
