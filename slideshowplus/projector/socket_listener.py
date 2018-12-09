import socket
import threading


def handle_client(client, address):
    print("handle_client()")
    size = 1024
    while True:
        data = client.recv(size)
        if data:
            response = data
            client.send(response)
            print(response)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # addr = ("localhost", 4352) # PJLink, Casio
    addr = ("localhost", 23)  # rs232 over ip, Epson
    s.bind(addr)
    s.listen(5)

    while True:
        client, addr = s.accept()
        ct = threading.Thread(
            target=handle_client,
            args=(client, addr)
        )
        ct.start()
