import socket
import threading
import sys
import time
from datetime import datetime
import struct
import pathlib



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
                print(data.decode('utf-8'))

    def verificar_chave_cliente(self, chave) -> bool:
        print(self.path)
        
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
        self.sock.sendall(b'ENVIAR A CHAVE PUBLICA AQUI')
        # ESTA VARIÁVEL DEVERÁ SER DECRIPTOGRAFADA UTILIZANDO A CHAVE PRIVADA DESTE CLIENTE.
        data = self.sock.recv(2048)
        return data.decode()
    

recv = threading.Thread(target=UDPServer().listen)
send = threading.Thread(target=UDPClient(ip=socket.gethostbyname(socket.gethostname()),
                                         port=5001).speak)


recv.start()
send.start()