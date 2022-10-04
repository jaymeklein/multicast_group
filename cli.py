import socket


class UDPClient:
    mcast_group = '10.151.34.113'
    mcast_port = 5001
    mcast_ttl = 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, mcast_ttl)
    sock.sendto(b'robot', (mcast_group, mcast_port))


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


a = TCPClient(ip='10.1.1.156', port=5000)
