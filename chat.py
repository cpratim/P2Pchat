from Crypto.Cipher import AES
from Crypto import Random
from config import IPADRESS, PORT, PASSPHRASE, YOURIP
from threading import Thread
import socket
import random
import hashlib
import sys
import base64


class Encryption():

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class Client():

    def __init__(self):
        self.host = IPADRESS
        self.port = PORT
        self.encryption = Encryption(PASSPHRASE)
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        print('Connected to {}'.format(self.host))

    def send_messages(self):
        while True:
            message = input('')
            message = self.encryption.encrypt(message)
            self.sock.send(message)

    def get_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                data = self.encryption.decrypt(data)
                print(("{}: {}").format(self.host, str(data)))
            except:
                pass

    def start(self):
        smthrd = Thread(target=self.send_messages)
        gmthrd = Thread(target=self.get_messages)
        gmthrd.start()
        smthrd.start()


class Server():

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = PORT
        self.encryption = Encryption(PASSPHRASE)
        self.sock = socket.socket()
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.connection, self.address = self.sock.accept()
        print("Connected to: {}".format(self.address[0]))

    def get_messages(self):
        while True:
            try:
                data = self.connection.recv(1024)
                if not data:
                    break
                data = self.encryption.decrypt(data)
                print(("{}: {}").format(self.address[0], str(data)))
            except:
                pass

    def send_messages(self):
        while True:
            message = input('')
            message = self.encryption.encrypt(message)
            print(message)
            self.connection.send(message)

    def start(self):
        smthrd = Thread(target=self.send_messages)
        gmthrd = Thread(target=self.get_messages)
        smthrd.start()
        gmthrd.start()

def run():
    try:
        Client().start()
    except:
        Server().start()

if __name__ == '__main__':
    run()
