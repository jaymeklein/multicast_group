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
    ip =  '10.151.34.113'
    # socket.gethostbyname(socket.gethostname())  # ip da máquina onde este código está rodando.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('10.151.34.113', port))
    mreq = struct.pack('4sl', socket.inet_aton('224.1.1.1'), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def __init__(self):
        pass

    def listen(self):

        while True:
            print(self.sock.recv(2048))

class tcp_server:
    port = 5002
    ip = '10.151.34.113'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print(f"Conexão inicial realizada por: {addr}.")

        while True:
            data = conn.recv(2048)
            if not data:
                break
            # Verificar se a chave pública enviada pelo cliente está na lista de chaves previamente cadastradas.
            conn.sendall(data)

tcp_server()