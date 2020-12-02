import socket
import tqdm
import os

# device's IP address
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001

# receiver 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = '<SEPARATOR>'

# create the server socket
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f'[*] Listening as {SERVER_HOST}:{SERVER_PORT}')

# accept connection if there is any
client_socket, address = s.accept()
# if below code is executed, that means the sender is connected
print(f'[+] {address} is connected.')

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, file_size = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
file_size = int(file_size)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(file_size), f'Receiving {filename}', unit='B', unit_scale=True, unit_divisor=1024)
# f = open('receiver/' + filename, 'wb')
with open('decrypt/' + filename, 'wb') as f:
    for _ in progress:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)

        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # upgrade the progress bar
        progress.update(len(bytes_read))

# clos the client socket
client_socket.close()
# close the sever socket
s.close()