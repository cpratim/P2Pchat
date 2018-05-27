from config import IPADRESS, PORT, PASSPHRASE, YOURIP
from flask import Flask, render_template, request
from threading import Thread
import socket
import random
import sys


class Client():

    def __init__(self):
        self.host = IPADRESS
        self.port = PORT
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        print('Connected to {}'.format(self.host))

    def send_messages(self):
        while True:
            message = input('')
            self.sock.send(message.encode('utf-8'))

    def get_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(("{}: {}").format(self.host, str(data.decode())))
            except:
                pass

    def start(self):
        smthrd = Thread(target=self.send_messages)
        gmthrd = Thread(target=self.get_messages)
        gmthrd.start()
        smthrd.start()


class Server():

    def __init__(self):
        self.host = YOURIP
        self.port = PORT
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
                print(("{}: {}").format(self.address[0], str(data.decode())))
            except:
                pass

    def send_messages(self):
        while True:
            message = input('')
            self.connection.send(message.encode())

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
