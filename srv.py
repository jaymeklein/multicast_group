import socket
import threading
import sys
import time
from datetime import datetime
import struct


class server_thread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print('Starting' + self.name)


class udp_server:
    port = 5001
    ip = '10.1.1.156'
    #  socket.gethostbyname(socket.gethostname()) # ip da máquina onde este código está rodando.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('10.1.1.156', port))
    mreq = struct.pack('4sl', socket.inet_aton('224.1.1.1'), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def __init__(self):
        pass

    def listen(self):

        while True:
            print(self.sock.recv(2048))


class TCPServer:
    sock = None

    def __init__(self, port: int = 5000) -> None:
        self.ip = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, port))

    def listen(self) -> str:
        self.sock.listen()
        conn, addr = self.sock.accept()
        with conn:
            print(f"Conexão inicial realizada por: {addr}.")

            data = conn.recv(2048)

            if data:

                # Verificar se a chave pública enviada pelo cliente está na lista de chaves previamente cadastradas.
                conn.sendall(data)
                return data.decode()


