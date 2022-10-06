import os
import socket
import threading
import sys
import time
from datetime import datetime
import struct
import pathlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP



class UDPServer:
    port = 5001
    ip = socket.gethostbyname(socket.gethostname())
    #  socket.gethostbyname(socket.gethostname()) # ip da máquina onde este código está rodando.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    mreq = struct.pack('4sl', socket.inet_aton('224.1.1.1'), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def __init__(self):
        pass

    def listen(self):
        while True:
            data = self.sock.recv(2048).decode('utf-8')
            print(f'Received message -> {data}')


class TCPServer:
    sock = None
    path = pathlib.Path(__file__).parent.resolve()
    path_keys = str(path) + '\\keys'

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
                # print(data.decode('utf-8'))
                print(self.verificar_chave_cliente(data.decode('utf-8')))

    def verificar_chave_cliente(self, chave) -> bool:
        keys = os.listdir(self.path_keys)
        for key in keys:
            with open(self.path_keys + f'\\{key}', 'r') as file:
                f = file.read()
                if f == chave:
                    # RESPONDER AO CLIENTE TCP, A CHAVE SIMÉTRICA CRIPTOGRAFADA COM
                    # A CHAVE PÚBLICA RECEBIDA
                    return True

        return False


        
class UDPClient:
    mcast_group = '10.151.34.113'
    mcast_port = 5001
    mcast_ttl = 2

    
    def __init__(self, ip, port):
        self.mcast_group = ip
        self.mcast_port = port        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.mcast_ttl)
        self.sock.settimeout(15)
    
    def speak(self):
        while True:
            msg = input('Digite uma mensagem ao grupo multicast -> ').encode('utf-8')
            self.sock.sendto(msg, (self.mcast_group, self.mcast_port))
            


class TCPClient:
    sock = None
    path = pathlib.Path(__file__).parent.resolve()
    path_keys = str(path) + '\\client_keys'

    def __init__(self, ip: str = '127.0.0.1', port: int = 5000) -> None:
        """
        :param ip: Ip da máquina onde o servidor TCP está sendo executado.
        :param port: Porta vinculada ao parâmetro anterior do servidor TCP.
        """
        self.ip = ip
        self.port = port

    def conexao_inicial(self) -> str:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        with open(self.path_keys + '\\public_key_1.PEM', 'r') as file:
            file = file.read().encode('utf-8')
            self.sock.sendall(file)
            # ESTA VARIÁVEL DEVERÁ SER DECRIPTOGRAFADA UTILIZANDO A CHAVE PRIVADA DESTE CLIENTE.
            data = self.sock.recv(2048)
            return data.decode()

    def gera_par_chaves(self, client_id) -> None:
        private_key = RSA.generate(1024)
        public_key_file = private_key.publickey()
        diretorio_cliente = self.path_keys

        prv_key = private_key.exportKey(format='PEM')
        pub_key = public_key_file.exportKey(format='PEM')

        try:
            os.makedirs(diretorio_cliente)
        except FileExistsError:
            pass
        try:
            os.makedirs(self.path_keys)
        except FileExistsError:
            pass

        public_key_file = open(f'{self.path_keys}\\public_key_{client_id}.PEM', 'wb')
        public_key_file.write(pub_key)
        public_key_file.close()

        private_key_file = open(f'{self.path_keys}\\private_key_{client_id}.PEM', 'wb')
        private_key_file.write(prv_key)
        private_key_file.close()


recv = threading.Thread(target=UDPServer().listen)
send = threading.Thread(target=UDPClient(ip=socket.gethostbyname(socket.gethostname()),
                                         port=5001).speak)


# recv.start()
# send.start()

tserver = TCPServer().listen()
tclient = TCPClient()

