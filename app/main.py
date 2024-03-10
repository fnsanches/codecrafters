# Uncomment this to pass the first stage
import socket
import threading
import sys

def main():
    print("Logs from your program will appear here!")
    while True:
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        thr = threading.Thread(target= handle_connection, args=(server_socket, dir,))
        thr.start()

def handle_connection(server_socket, dir):
    server_socket.listen(1)
    conn, addr = server_socket.accept() # wait for client
    data = conn.recv(1024).decode().split("\r\n")
    method, path, http_protocol = data[0].split()
    if data[1]:
        host = data[1].split(": ")[1]
    if data[2]:
        user_agent = data[2].split(": ")

    if path == "/":
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif path.startswith("/files/"):
        file_name = path.split("/files/")[1]
        full_path = f"{dir}/{file_name}"
        try:
            with open(full_path, "rb") as file:
                file_content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n{file_content}"
                conn.sendall(response.encode())
        except FileNotFoundError:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    elif path.startswith("/echo/"):
        msg = path.split("/echo/")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}"
        conn.sendall(response.encode())
    elif path.startswith("/user-agent"):
        msg = user_agent[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}"
        conn.sendall(response.encode())
    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    conn.close()



if __name__ == "__main__":
    dir = ""
    if len(sys.argv) >= 3:
        dir = sys.argv[2]
    main(dir)
