import socket

class udp_client:
    mcast_group = '10.151.34.113'
    mcast_port = 5001
    mcast_ttl = 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, mcast_ttl)
    sock.sendto(b'robot', (mcast_group, mcast_port))

    def __init__(self):
        pass

class tcp_client:
    ip = '10.151.34.113'
    port = 5002
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    # Implementar envio da chave pública deste cliente.
    sock.sendall(b'JOIN')
    data = sock.recv(2048)
    print(f'Received {data}')

    def __init__(self):
        pass

tcp_client()