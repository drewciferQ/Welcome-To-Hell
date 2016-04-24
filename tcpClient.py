import socket

host = "127.0.0.1"
port = 9999
message = "AAABBBCCC"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.sendto(message.encode(), (host, port))
data, addr = client.recvfrom(4096)
print(data)
