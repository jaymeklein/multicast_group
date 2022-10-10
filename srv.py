import json
from json import dumps
import os
import socket
import threading
import sys
import time
import tkinter
from datetime import datetime
import struct
import pathlib
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from tkinter import *
from tkinter import filedialog
chave_simetrica = 'nao consegui'


class UDPServer:
    port = 5001
    ip = socket.gethostbyname(socket.gethostname())
    #  socket.gethostbyname(socket.gethostname()) # ip da máquina onde este código está rodando.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    mreq = struct.pack('4sl', socket.inet_aton('224.1.1.1'), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    last_msg = b'None'

    ultimo_lance = {
        'item': 'celtinha rebaixado',
        'valor': 1000.00,
        'tempo_inicio': time.time(),
        'tempo_fim': time.time() + 120,
        'finalizado': False
    }
    connections = set()


    def __init__(self):
        pass

    def listen(self):
        print(f'IP UDP: {self.ip}\nPort UDP: {self.port}\n')
        self.ultimo_lance['tempo_restante'] =  self.ultimo_lance['tempo_fim'] - time.time()

        while self.ultimo_lance['tempo_restante'] > 0:
             
            self.ultimo_lance['tempo_restante'] = self.ultimo_lance['tempo_fim'] - time.time()

            try:
                data, comm = self.sock.recvfrom(2048)

                if data.decode('utf-8') == 'JOIN':
                    self.connections.add(comm)

                    if self.ultimo_lance:
                        self.sock.sendto(dumps(self.ultimo_lance).encode(), comm)

                else:
                    print(f'Received message -> {data}\nFrom -> {comm}')

                    self.ultimo_lance['valor'] = data.decode()

                    for connection in self.connections:
                        self.sock.sendto(dumps(self.ultimo_lance).encode(), connection)

            except ConnectionResetError:
                if comm in self.connections:
                    self.connections.remove(comm)
                continue

            pass
        
        for connection in self.connections:
            self.ultimo_lance['finalizado'] = True
            self.sock.sendto(dumps(self.ultimo_lance).encode(), connection)

        return None

class TCPServer:
    last_msg = None
    sock = None
    path = pathlib.Path(__file__).parent.resolve()
    path_keys = str(path) + '\\keys'

    def __init__(self, port: int = 5000) -> None:
        self.ip = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.sock.bind((self.ip, port))

    def listen(self) -> str:
        print(f'\nIP TCP: {self.ip}\nPort TCP: {self.port}\n')
        while True:
            self.sock.listen()
            conn, addr = self.sock.accept()
            with conn:
                print(f"Conexão inicial TCP realizada por: {addr}.")

                data = conn.recv(2048)


                if data:

                    if data == self.last_msg:
                        continue

                    data = self.verificar_chave_cliente(data.decode('utf-8'))
                    # Verificar se a chave pública enviada pelo cliente está na lista de chaves previamente cadastradas.
                    if data:

                        dict_join = {
                            'ip': socket.gethostbyname(socket.gethostname()),
                            'port': 5001,
                            'symmetric': chave_simetrica
                        }
                        print(data)
                        ciphertext = self.encrypt(dumps(dict_join), data)
                        conn.sendall(ciphertext)
                        self.last_msg = ciphertext
                    else:
                        conn.sendall(b'putz mano tua chave nao ta com nois.')
    def encrypt(self, texto, chave_publica):
        with open(chave_publica, "rb") as file:
            chave_publica = RSA.importKey(file.read())

        rsa_cipher = PKCS1_OAEP.new(chave_publica)
        ciphertext = rsa_cipher.encrypt(texto.encode())

        return ciphertext

    def verificar_chave_cliente(self, chave) -> bool:
        keys = os.listdir(self.path_keys)
        for key in keys:
            with open(self.path_keys + f'\\{key}', 'r') as file:
                f = file.read()
                if f == chave:
                    # RESPONDER AO CLIENTE TCP, A CHAVE SIMÉTRICA CRIPTOGRAFADA COM
                    # A CHAVE PÚBLICA RECEBIDA
                    return file.name

        return False



# recv = threading.Thread(target=UDPServer().listen)
# send = threading.Thread(target=UDPClient(ip=socket.gethostbyname(socket.gethostname()),
#                                          port=5001).speak)

# recv.start()
# send.start()

tcp = threading.Thread(target=TCPServer().listen)
udp = threading.Thread(target=UDPServer().listen)

tcp.start()
udp.start()
