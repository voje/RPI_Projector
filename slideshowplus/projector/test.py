import socket

try_port = 23
ip = "192.168.2.22"
print("Trying port {}.".format(try_port))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(0)
s.settimeout(2)
s.connect((ip, try_port))
s.send(b"Luka je prejel kopje v koleno.\n")
response = s.recv(1024)
s.close()
print(response)
