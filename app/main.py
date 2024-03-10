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
        data = conn.recv(1024).decode()
        method, host, user_agent = data.split("\r\n")


        path = method.split()[1]
        if path == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        elif path.startswith("/echo/"):
            msg = path.split("/echo/")[1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}"
            conn.sendall(response.encode())
        elif path.startswith("/user_agent"):
            msg = user_agent.split(": ")[1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}"
            conn.sendall(response.encode())
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
        conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
