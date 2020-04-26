import socket
from pickle import loads, dumps


class Pipe:
    def __init__(self, server: str, port: int) -> None:
        self.server = server
        self.port = port
        self.tcp = socket.socket()
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connected = False
        self.username = None
        self.udp_password = None
        self.game_port = None

    def connect(self) -> bool:
        try:
            self.tcp.connect((self.server, self.port))
            self.connected = True
            return True
        except (ConnectionResetError, ConnectionRefusedError):
            return False

    def login(self) -> bool:

        if not self.connected:
            success = self.connect()
            if not success:
                return False

        self.tcp.send(f"play request,,1234509876".encode())
        response = self.tcp.recv(100)

        if response == b"Pended":
            return True
        else:
            return False

    def await_response(self) -> list:
        try:
            data = self.tcp.recv(1000)
            data = data.decode().split("||")
            full_data = []

            for seg in data:
                seg = seg.split(",,")
                full_data += seg
                if seg[0] == "Start":
                    self.username = seg[1]
                    self.game_port = int(seg[2])

            return full_data
        except ConnectionResetError:
            return [False]

    def transport(self, game_data: list) -> tuple:
        game_data = [self.username] + game_data

        game_data = (dumps(game_data)) + b"||||"

        self.udp.sendto(game_data, (self.server, self.game_port))

        data, _ = self.udp.recvfrom(100)
        data = data.split(b"||||")

        if len(data) > 1:
            data = loads(data[0])

            return True, data
        else:
            return False, None
