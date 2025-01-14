import socket
import sys

HOST = None
PORT = 80
s = None

for res in socket.getaddrinfo(
    HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE
):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
        s.bind(sa)
        s.listen(1)
    except OSError as e:
        print(f"Error: {e}")
        s.close()
        s = None
        continue
    break

print(f"Listening on port {PORT}...")

conn, addr = s.accept()
with conn:
    print("Connected by", addr)
    
    data = conn.recv(1024)
    print("Received data:", data.decode())

    response_body = b"Hello Browser"
    response_headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    
    conn.sendall(response_headers.encode() + response_body)

print("Response sent successfully!")
