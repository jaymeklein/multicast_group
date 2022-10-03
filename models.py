class ClienteModel:

	def __init__(self, address, port, id):
		self.__address: str = address
		self.__port: int = port
		self.__id: int = id
		self.__keys: set = set()

	@property
	def address(self):
		return self.__address

	@property
	def port(self) -> int:
		return self.__port

	@property
	def id(self):
		return self.__id

	def add_keys(self, keys) -> None:
		self.__keys = keys


class ClientData:
	def __init__(self, address, port, id):
		self.__address: str = address
		self.__port: int = port
		self.__id: int = id


class MessageModel:
	def __init__(self):
		self.__data = {
			'msg_type': None,
			'msg': None
		}

	def data(self, msg_type: str, msg: dict = None) -> str:
		msg_types = ('JOIN', 'BID', 'MESSAGE')
		if msg_type in msg_types:
			self.__data = {
				'msg_type': msg_type,
				'msg': msg
			}
			msg = str(self.__data).encode('utf-8')
			return msg

		else:
			return b''

