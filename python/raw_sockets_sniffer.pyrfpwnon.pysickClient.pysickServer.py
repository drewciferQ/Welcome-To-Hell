import socket
import sys

# Create tcp, ip handlers.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prevent from "address already in use" shit.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Assign some wild shit for these roudy ass loud mouths!!
server_address = ("localhost", 8081)
print 'starting up on %s port %s' % server_address
server.bind(server_address)

# Start peepin nugguh.
server.listen(5)

# Wait nuggah...
connection, client_address = server.accept()
print 'connection from', connection.getpeername()

# Reception bitches.
data = connection.recv(4096)
if data:
    print "Recieved ", repr(data)

    # Send it formatted.
    data = repr(data)
    data = data.rstrip()
    connection.send('%s\n%s\n%s\n' % ('-' * 80, data.center(80), '-' * 80))
    print "Response sent!!!"
connection.shutdown(socket.SHUT_RD | socket.SHUT_WR)
connection.close()
print "Fuck off now, ya here!!"
server.close()
