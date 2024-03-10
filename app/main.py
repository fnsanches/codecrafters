# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(1)
    while True:
        conn, addr = server_socket.accept() # wait for client
        data = conn.recv(1024).decode().split("\r\n")
        method, path, http_protocol = data[0].split()
        if data[1]:
            host = data[1].split(": ")[1]
        if data[2]:
            user_agent = data[2].split(": ")

        if path == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
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
    server_socket.close()


if __name__ == "__main__":
    main()
