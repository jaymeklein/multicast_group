import socket
import struct
import sys
from time import sleep
from json import dumps
from models import JoinModel, LanceModel


class client:
	multicast_group = '10.151.34.113'
	multicast_port = 5007
	multicast_ttl = 2

	def send(self, arg='', pem_file=''):
		sock = socket.socket(socket.AF_INET,
							socket.SOCK_DGRAM,
							socket.IPPROTO_UDP)

		sock.setsockopt(socket.IPPROTO_IP,
						socket.IP_MULTICAST_TTL,
						self.multicast_ttl)

		if arg == '':
			arg = b'HOO YEEEEAAAH'

		sock.sendto(arg.encode('UTF-8'), (self.multicast_group, self.multicast_port))



	def lance(self, item_id, valor, private_key):
		lance=''
		return dumps(lance)
	



if __name__ == "__main__":
	client = client()
	join = JoinModel()
	join.multicast_group = ''
	join.multicast_port = ''
	join.pem_file = None

	client.send('asdasd')