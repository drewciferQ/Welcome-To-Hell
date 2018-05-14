#!/usr/bin/python
import sys
import socket
import getopt
import threading
import subprocess

# global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):

        file_buffer = ""

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # now write out those bytes...
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # acknowledge the write out
            client_socket.send('Successfully saved file to %s\r\n' % upload_destination)
        except:
            client_socket.send('Failed to save file to %s\r\n' % upload_destination)

    # check for command execution
    if len(execute):
        output = run_command(execute)

        client_socket.send(output)

    # now another loop if shell was requested.
    if command:

        while True:
            client_socket.send('<aocat:#> ')

            # Recieve until we see a linefeed;
        cmd_buffer = ""
        while '\n' not  in cmd_buffer:
            cmd_buffer += client_socket.recv(1024)

        response = run_command(cmd_buffer)

        client_socket.send(response)


def run_command(command):

    # Trim the newline.
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = 'Failed to execute command.\r\n'

    # send somethin back
    return output


def server_loop():

    global target

    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)
        while True:

            # now collect data back.
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print response,

            # wait for more....
            buffer = raw_input("")
            buffer += '\n'
            client.send(buffer)
    except:

        print '[*] Exception! Exiting..'
        client.close()


def usage():
    print 'Andrew Net Tool'
    print
    print 'Usage: aocat.py -t target_host -p port'
    print '-l --listen          -listen on [host]:[port] for incoming connections'
    print '-e --execute=file    -execute the given file upon connection'
    print '-c --command         -initialize a command shell'
    print '-u --upload=dest.    -upload file upon connection and write to [destination]'
    sys.exit(0)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the command line args
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hle:t:p:cu:', ['help','listen','execute','target','port','command','upload'])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ('-h','--help'):
            usage()
        elif o in ('-l','--listen'):
            listen = True
        elif o in ('-e','--execute'):
            execute = a
        elif o in ('-c','--command'):
            command = True
        elif o in ('-u','--upload'):
            upload_destination = a
        elif o in ('-t','--target'):
            target = a
        elif o in ('-p','--port'):
            port = int(a)
        else:
            assert  False,'Unhandled Option'

    # are we gonna listen or just send data??
    if not listen and len(target) and port > 0:
        # read in the buffer.
        # this will block, so ctrl-D if no go.
        buffer = sys.stdin.read()

        # send data!!
        client_sender(buffer)

    # are we going to listen and try and upload?
    # or drop shell script perhaps...?
    if listen:
        server_loop()


if __name__ == '__main__':
        main()










