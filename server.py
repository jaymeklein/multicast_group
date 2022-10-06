import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
from os import makedirs
from models import *
import yaml


class Server:

	def __init__(self):
		self.dict_auction = None
		self.multicast_group = socket.gethostbyname(socket.gethostname())
		self.path = os.path.abspath(os.getcwd())
		self.multicast_port = 5001
		self.tcp_port = 5002
		self.symmetric_key = 'ROBSONCOSTA'
		self.is_all_groups = True
		self.clients_data = None
		self.clients = set()
		self.udp_sock = None
		self.tcp_sock = None
		self.clients_data = set()
		cli01 = ClienteModel(address=self.multicast_group,
		                     port=self.multicast_port,
		                     id=1)
		self.add_client(cli01,
		                c_data=(cli01.address, cli01.port))
		self.key = RSA.importKey(open(self.path + '\\client_1\\public_key.PEM').read(),
		                         passphrase=self.symmetric_key)
		self.cipher = PKCS1_OAEP.new(self.key)

	def listen(self) -> None:
		self.udp_socket_opts()
		self.tcp_socket_opts()
		print(f'Multicast Group: {self.multicast_group}, {self.multicast_port}')
		print(f'TCP P2P: {self.multicast_group}, {self.tcp_port}')

		while True:
			try:
				self.tcp_sock.listen()
				conn, src_tcp = self.tcp_sock.accept()

				with conn:
					data = conn.recv(2048)
					self.join_via_tcp(data, src_tcp)
					self.send_msg('MESSAGE',
					              (self.multicast_group,
					               self.multicast_port),
					              'TCP',
					              conn=conn)
					conn.close()

			except TimeoutError:
				pass

			try:
				data, cli = self.udp_sock.recvfrom(2048)
				self.receive_messages_udp(data)

			except (TimeoutError, AttributeError, BaseException):
				pass

	def auction(self, new_bid=None, current_user=None) -> dict:
		self.dict_auction = {
			'item': 'celtinha',
			'starting_bid': 1000.00,
			'current_bid': new_bid if new_bid else None,
			'current_user': current_user if current_user else None
		}
		return self.dict_auction

	def join_via_tcp(self, data, src_tcp) -> None:

		if data:
			data = yaml.safe_load(data.decode('utf-8'))

			if 'msg_type' in data:
				client = ClienteModel(address=src_tcp[0],
				                      port=src_tcp[1],
				                      id=len(self.clients) + 1)

				c_data = (client.address, client.port)

				if data['msg_type'] == 'JOIN' and c_data not in self.clients_data:
					self.add_client(client, c_data)

	def receive_messages_udp(self, data) -> None:

		if data:
			data = yaml.safe_load(data.decode('utf-8'))

			if 'msg_type' not in data:
				return None

			else:
				if data['msg_type'] == 'BID':
					# CRIAR MÉTODO PARA REGISTRAR O LANCE NOVO
					print(data['msg'])

				elif data['msg_type'] == 'MESSAGE':
					print(data['msg'])

	def udp_socket_opts(self) -> None:
		self.udp_sock = socket.socket(socket.AF_INET,  # IPv4
		                              socket.SOCK_DGRAM,  # UDP
		                              socket.IPPROTO_UDP)
		# self.udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP)

		self.udp_sock.bind((self.multicast_group,
		                    self.multicast_port))
		self.udp_sock.settimeout(10)

	def tcp_socket_opts(self) -> None:
		self.tcp_sock = socket.socket(socket.AF_INET,  # IPV4
		                              socket.SOCK_STREAM)  # TCP

		self.tcp_sock.bind((self.multicast_group,
		                    self.tcp_port))
		self.tcp_sock.settimeout(1)

	def add_client(self, client, c_data) -> None:
		self.clients_data.add(c_data)
		self.clients.add(client)
		keys = self.generate_keys(client)
		client.add_keys(keys)

	def generate_keys(self, client) -> tuple:

		private_key = RSA.generate(1024)
		public_key_file = private_key.publickey()
		diretorio_cliente = f'{self.path}\\client_{client.id}'

		prv_key = private_key.exportKey(format='PEM', passphrase=self.symmetric_key)
		pub_key = public_key_file.exportKey(format='PEM', passphrase=self.symmetric_key)

		try:
			makedirs(diretorio_cliente)
		except FileExistsError:
			pass

		public_key_file = open(f'{self.path}\\client_{client.id}\\public_key.PEM', 'wb')
		public_key_file.write(pub_key)
		public_key_file.close()

		private_key_file = open(f'{self.path}\\client_{client.id}\\private_key.PEM', 'wb')
		private_key_file.write(prv_key)
		private_key_file.close()

		return pub_key, prv_key

	def send_msg(self, msg_type, msg=None, socket_type='UDP', conn=None):
		msg = MessageModel().data(msg_type=msg_type, msg=msg)

		if socket_type == 'UDP':
			msg = self.cipher.encrypt(msg)
			self.udp_sock.sendto(msg,
			                     (self.multicast_group,
			                      self.multicast_port))

		elif socket_type == 'TCP':
			print(f'New message:\n{msg}')
			msg = self.cipher.encrypt(msg)
			print(f'Encrypted message:\n{msg}')
			conn.sendall(msg)


if __name__ == "__main__":
	server = Server()
	server.listen()
