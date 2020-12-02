import socket
import tqdm
import os

SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 4096      # send 4096 bytes each time step

# the ip address or hostname server, the receiver
host = '127.0.0.1'
# the port, let's use 5001
port = 5001

# the name of file we want to send, make sure it exists
f = open('config.txt', 'r')
filename = f.read() + '.encrypted'
f.close()

file_path = 'encrypt/' + filename
# get the file size
file_size = os.path.getsize(file_path)

s = socket.socket()
print(f'[+] Connecting to {host}:{port}')
s.connect((host, port))
print(f'[+] Connected.')

# send the filename and file_size
s.send(f'{filename}{SEPARATOR}{file_size}'.encode())

# start sending the file
progress = tqdm.tqdm(range(file_size), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)
with open(file_path, 'rb') as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transmission in busy networks
        s.sendall(bytes_read)
        # update the progess bar
        progress.update(len(bytes_read))

# close the socket
s.close()