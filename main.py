from aes import *
import os
import struct
import time


def file_decryption(key, input_filename, chunk_size=64 * 1024):
    output_filename = os.path.splitext(input_filename)[0]
    # output_filename = 'encrypt/data.txt'
    with open(input_filename, 'rb') as infile:
        original_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES(key)
        with open(output_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt_cfb(chunk, iv))
            outfile.truncate(original_size)


def file_encryption(key, input_filename, chunk_size=64 * 1024):
    output_filename = input_filename + '.encrypted'
    iv = os.urandom(16)
    encryptor = AES(key)
    filesize = os.path.getsize(input_filename)
    with open(input_filename, 'rb') as infile:
        with open(output_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                    print(chunk)
                outfile.write(encryptor.encrypt_cfb(chunk, iv))


def main():
    before = time.time()

    f = open('config.txt', 'r')
    filename = f.read()
    f.close()

    file_path = 'encrypt/' + filename
    # file_path = 'decrypt/' + filename + '.encrypted'

    master_key = 'abcdefghij123456'
    file_encryption(master_key, file_path)
    # file_decryption(master_key, file_path)
    print('Time elapsed: ', time.time() - before)


if __name__ == '__main__':
    main()
