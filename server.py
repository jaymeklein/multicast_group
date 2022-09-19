import socket
import struct
from time import sleep
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from Crypto.PublicKey import RSA
import os
from os import makedirs


class Server:

	def __init__(self):
		self.multicast_group = '10.151.34.113'
		self.path = os.path.abspath(os.getcwd())
		self.multicast_port = 5007
		self.is_all_groups = True
		self.public_key = None
		self.clients = []

	def listen(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.bind((self.multicast_group, self.multicast_port))

		print(f'Listening on: {self.multicast_group}, {self.multicast_port}')


		while True:
			sleep(1)
			data, server = self.sock.recvfrom(1024)


			client = {
				'address': server[0],
				'port': server[1],
				'id': len(self.clients)+1,
				'keys': None
			}

			if client not in self.clients:
				self.send_msg("{} has joined the auction.".format(client['address']))
				client['key'] = self
				self.clients.append(client)
				print(self.clients)

			
			print(f'Received: {data}')


	def generate_keys(self, client):
    		
		private_key = RSA.generate(1024)
		public_key_file = private_key.publickey()
		diretorio_cliente = f'{self.path}\\client_{client["id"]}'

		prv_key = '-----BEGIN CERTIFICATE-----\n' + str(private_key.exportKey(format='PEM')) + '\n-----END CERTIFICATE-----'
		pub_key = '-----BEGIN CERTIFICATE-----\n' + str(public_key_file.exportKey(format='PEM')) + '\n-----END CERTIFICATE-----'

		
		try:
			makedirs(diretorio_cliente)
		except FileExistsError:
			pass

		public_key_file = open(f'{self.path}\\client_{client["id"]}\\public_key.PEM', 'w')
		public_key_file.write(pub_key)
		public_key_file.close()

		private_key_file = open(f'{self.path}\\client_{client["id"]}\\private_key.PEM', 'w')
		private_key_file.write(prv_key)
		private_key_file.close()

	
	def send_msg(self, msg):
    		self.sock.sendto(bytes(msg,'utf-8'),
							(self.multicast_group, self.multicast_port))
	

if __name__ == "__main__":
	server = Server()
	# server().listen()
	server.generate_keys({'id': 12312512})
