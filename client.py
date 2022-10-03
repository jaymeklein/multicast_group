import socket
import struct
import sys
from time import sleep
from json import dumps
import os
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from models import *
import yaml


class Client:

	multicast_group = '192.168.0.109'
	multicast_port = None
	tcp_port = 5002
	multicast_ttl = 2
	public_key = None
	private_key = None

	def __init__(self):
		self.path = os.path.abspath(os.getcwd())
		self.sock = None
		self.symmetric_key = 'ROBSONCOSTA'
		self.key = RSA.importKey(open(self.path + '\\client_1\\private_key.PEM').read(),
		                         passphrase=self.symmetric_key)
		self.cipher = PKCS1_OAEP.new(self.key)
		self.data = None

	def udp_socket_opts(self) -> None:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.multicast_ttl)
		self.sock.settimeout(5)

	def tcp_join(self) -> None:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.multicast_group, self.tcp_port))
		s.sendall(MessageModel().data(msg_type='JOIN'))

		while True:
			self.data = s.recv(2048)
			if self.data != b'':
				self.data = self.cipher.decrypt(self.data)
				self.data = yaml.safe_load(self.data)
				self.multicast_port = self.data[1]
				self.multicast_group = self.data[0]
				break

	def listen_auction(self) -> None:
		self.udp_socket_opts()
		while True:
			try:
				sleep(2)
				data, srv = self.sock.recvfrom(2048)
				break

			except TimeoutError:
				continue

	def send(self, msg) -> None:
		"""
		:param msg: message string
		"""
		self.sock.sendto(msg.encode('UTF-8'), (self.multicast_group, self.multicast_port))



if __name__ == "__main__":
	connection = Client()
	connection.tcp_join()
	connection.listen_auction()
	print('done')
	# connection.join()
