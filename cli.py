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
from cryptography.fernet import Fernet
from tkinter import *
from tkinter import filedialog
from json import loads, dumps
import time


class UDPClient:
	mcast_ttl = 2

	def __init__(self, mcast_group, mcast_port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.mcast_ttl)
		self.sock.settimeout(3)
		self.mcast_group = mcast_group
		self.mcast_port = mcast_port
		self.chave_simetrica = None

	def send(self, message) -> tuple:
		self.sock.sendto(str(message).encode('utf-8'), (self.mcast_group, self.mcast_port))

	def receive(self, txt_lance_atual, txt_sem_lance) -> None:
		try:
			data, comm = self.sock.recvfrom(2048)
			data = loads(data.decode())
			self.valor_atual = data['valor']
			txt_lance_atual.configure(text=data, width=45)

		except TimeoutError:
			txt_sem_lance.configure(text='Não há lances novos.')
			pass

class GUI:
	sock = None
	path = pathlib.Path(__file__).parent.resolve()
	path_keys = str(path) + '\\client_keys'

	def __init__(self) -> None:
		self.public_key = None
		self.tcp_ip = None
		self.tcp_port = None
		self.udp_ip = None
		self.udp_port = None
		self.conectado = False

	def iniciar(self) -> None:
		self.gui_entra_leilao()

		if self.public_key:
			# {"ip": "192.168.0.109", "port": 5001, "symmetric": "ROBSO"}
			self.gui_leilao(ip_multicast=self.dados_leilao['ip'],
			                port_multicast=self.dados_leilao['port'],
			                chave_simetrica=self.dados_leilao['symmetric'])


	def conexao_inicial(self, ip, port) -> str:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			port = int(port)

		except (TypeError, ValueError):
			return None
			pass
		self.sock.connect((ip, port))
		self.sock.sendall(self.public_key.encode('utf-8'))
		data = self.sock.recv(2048)

		data = self.decrypt(self.private_key ,data)
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


	def click_entrar_leilao(self, msg_field, window, ip_tcp, port_tcp) -> None:
		# TODO: validação se foi possível ou não entrar no grupo multicast do leilão.
		ip = ip_tcp.get()
		port = port_tcp.get()

		try:
			port = int(port)
		except ValueError:
			msg_field.configure(text=f'Erro ao converter "{port}" para inteiro.', width=100)

		if not self.public_key:
			msg_field.configure(text='A chave PÚBLICA não foi fornecida.', width=100)

		if not self.private_key:
			msg_field.configure(text='A chave PRIVADA não foi fornecida.', width=100)

		else:
			try:
				res = self.conexao_inicial(ip, port)

				if res:
					self.dados_leilao = loads(res)
					window.destroy()

			except socket.gaierror:
				msg_field.configure(text='Não foi possível se conectar ao endereço informado.', width=150)
				msg_field.place(relx=0.1, rely=0.88)

			except ConnectionRefusedError:
				msg_field.configure(text='Conexão recusada pela máquina de destino.', width=150)
				msg_field.place(relx=0.1, rely=0.88)

	def abrir_arquivo_pem(self, window, btn_arquivo_pem) -> None:
		pem = filedialog.askopenfilename(title='Open PEM file.', filetypes=(("Pem files", "*.PEM"),))
		file = open(pem, 'r')
 # Arquivo PEM da chave pública do cliente
		chave_atual = file.read()
		if 'PRIVATE' in chave_atual:
			self.private_key = chave_atual
			self.lbl_nome_arquivo = Label(window, text=os.path.basename(file.name))
			self.lbl_nome_arquivo.place(relx=0.2, rely=0.60)

		elif 'PUBLIC' in chave_atual:
			self.public_key = chave_atual
			self.lbl_nome_arquivo = Label(window, text=os.path.basename(file.name))
			self.lbl_nome_arquivo.place(relx=0.2, rely=0.40)

		file.close()

	def gui_entra_leilao(self) -> None:
		window = Tk()
		window.title("Leilão")
		ico = tkinter.PhotoImage(file=r'C:\Users\jayme\Projects\multicast_group\Foto_Robson.jpg')
		window.wm_iconphoto(False, ico)

		window.geometry("200x300")
		window.resizable(width=False, height=False)

		lbl_ip_tcp = Label(window, text='IP TCP:')
		lbl_port_tcp = Label(window, text='Port TCP:')
		entry_ip_tcp = Entry(window, width=18)
		entry_ip_tcp.insert(0, str(socket.gethostbyname(socket.gethostname())))
		entry_port_tcp = Entry(window, width=18)
		entry_port_tcp.insert(0, '5000')
		msg_resposta_tcp = Message(window, width=35)
		btn_entrar_leilao = Button(window, text='Entrar no Leilão',
		                           command=lambda: self.click_entrar_leilao(msg_resposta_tcp,
		                                                                    window,
		                                                                    entry_ip_tcp,
		                                                                    entry_port_tcp),
		                           width=25)
		btn_pem_privado = Button(window, text='Chave Privada',
		                         command=lambda: self.abrir_arquivo_pem(window, btn_pem_privado),width=25)

		btn_pem_publico = Button(window, text='Chave Pública',
		                         command=lambda: self.abrir_arquivo_pem(window, btn_pem_publico), width=25)

		lbl_ip_tcp.place(relx=0.05, rely=0.01)
		entry_ip_tcp.place(relx=0.4, rely=0.01)

		lbl_port_tcp.place(relx=0.05, rely=0.11)
		entry_port_tcp.place(relx=0.4, rely=0.11)

		btn_pem_publico.place(relx=0.05, rely=0.27)
		btn_pem_privado.place(relx=0.05, rely=0.50)

		btn_entrar_leilao.place(relx=0.05, rely=0.77)
		msg_resposta_tcp.place(relx=0.2, rely=0.88)

		window.mainloop()
	def click_enviar_lance(self, entry, txt_field) -> None:
		txt_field.configure(text='')
		text = entry.get()
		text_button = self.btn_enviar_lance['text']
		self.txt_sem_lance.configure(text='')

		if text == '' and  text_button == 'Entrar no Grupo':
			self.lbl_rs.place(relx=0.5, rely=0.06)
			self.btn_receber_lances.configure(state=NORMAL)
			self.btn_enviar_lance.configure(text='Enviar Lance')
			self.udp.send('JOIN')

		elif text_button != 'Entrar no Grupo':


			try:
				value = float(entry.get())

			except ValueError:
				entry.delete(0, 'end')
				txt_field.configure(text=f"Erro ao converter \n'{text}'\n para float.", height=3)

				if self.udp.valor_atual + 10 > value:
					self.txt_sem_lance.configure('O valor fornecido deve ter no mínimo 10,00\n a mais do valor atual do item.',
					                             width=23,
					                             height=50)
					return None

				elif value >= self.udp.valor_atual + 10 :
					entry.delete(0, 'end')
					self.udp.send(value)


	def click_sair_app(self, window) -> None:
		window.destroy()

	def gui_leilao(self, ip_multicast: str, port_multicast: int, chave_simetrica: str) -> None:
		# print(f"IP: {ip_multicast}\nPORT: {port_multicast}\nSYMMETRIC KEY: {chave_simetrica}\n")
		self.udp = UDPClient(ip_multicast, port_multicast)
		self.udp.chave_simetrica = chave_simetrica
		window = Tk()
		window.title("Leilão")
		ico = tkinter.PhotoImage(file=r'C:\Users\jayme\Projects\multicast_group\Foto_Robson.jpg')
		window.wm_iconphoto(False, ico)
		window.resizable(width=False, height=False)
		window.geometry("450x450")

		lbl_item_atual = Label(window, text="Item atual")
		txt_lance_atual = Message(window, width=45, text='Respostas dos lances aqui')

		lbl_enviar_lance = Label(window, text="Valor do Lance Desejado")
		self.lbl_rs = Label(window, text='R$', anchor='e', state=DISABLED)

		entry_valor_lance = Entry(window, width=30)
		txt_resposta_lance = Label(window, width=23, height=1)

		self.txt_sem_lance = Label(window, width=23, height=3)


		self.btn_enviar_lance = Button(window,
		                               text='Entrar no Grupo',
		                               command=lambda: self.click_enviar_lance(entry=entry_valor_lance,
		                                                                       txt_field=txt_resposta_lance))
		self.btn_receber_lances = Button(window,
	                                     text='Receber Ultimo Lance',
	                                     width=25,
	                                     command=lambda: self.udp.receive(txt_lance_atual, self.txt_sem_lance),
	                                     state=DISABLED)

		btn_sair = Button(window, text='Sair', padx=42, command=lambda: self.click_sair_app(window))

		lbl_item_atual.place(relx=0.18, rely=0.01)
		txt_lance_atual.place(relx=0.01, rely=0.06)
		lbl_enviar_lance.place(relx=0.6, rely=0.01)

		entry_valor_lance.place(relx=0.55, rely=0.06)
		self.btn_enviar_lance.place(relx=0.55, rely=0.12)
		self.btn_receber_lances.place(relx=0.55, rely=0.34)
		txt_resposta_lance.place(relx=0.55, rely=0.18)
		self.txt_sem_lance.place(relx=0.55, rely=0.42)
		btn_sair.place(relx=0.6, rely=0.9)

		window.mainloop()

	def decrypt(self, chave_privada, texto_criptografado):
		chave_privada = RSA.importKey(chave_privada, 'MyPassphrase')
		rsa_cipher = PKCS1_OAEP.new(chave_privada)
		decrypted_text = rsa_cipher.decrypt(texto_criptografado)

		return decrypted_text


cli = GUI().iniciar()
# cli = GUI().iniciar()
