import socket
from threading import Thread
from random import randint
from pickle import loads, dumps
import multiprocessing


# players connection entry point
def player_entry() -> None:
    while True:
        conn, _ = sock.accept()

        # creates a separate thread for each
        # player that connects
        player = Thread(target=login_entry, args=[conn])
        player.start()


# an entry for players to create or join game rooms
def login_entry(conn) -> None:
    global udp_port
    global team

    # receives connection parameters from player
    data = conn.recv(100)
    data = (data.decode("utf-8")).split(",,")

    if data == ["play request", "1234509876"]:
        conn.send(b"Pended")
        team.append(conn)
        for _player_ in team:
            _player_.send(f"Team count,,{len(team)}||".encode())
        if len(team) == 3:
            room = multiprocessing.Process(
                target=game_room, args=(team, udp_port, host,)
            )
            room.start()
            team = []
            udp_port += 4


def game_room(teammates: list, ports: int, _host_: str) -> None:
    udp = None

    while True:
        try:
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp.bind((_host_, ports))
            break
        except OSError:
            ports += 1
            continue

    for i, _player_ in enumerate(teammates):
        _player_.send(f"Start,,{i},,{ports}||".encode())

    sent_player = []
    wall_pos = 400

    pipe = {"0": [], "1": [], "2": []}

    while True:
        data, address = udp.recvfrom(1024)
        data = data.split(b"||||")

        if len(data) > 1:
            data = loads(data[0])

            if data[0] in sent_player:
                wall_pos = randint(10, 600)
                sent_player = [data[0]]
            else:
                sent_player.append(data[0])

            # pasting game data in pipe
            for _player_ in pipe.keys():
                if len(data) > 2:
                    if data[0] != _player_:
                        if len(pipe[_player_]) == 2:
                            pipe[_player_].pop(0)
                        pipe[_player_].append(data[1:])

            # checking if viable data is available to be sent
            if pipe[data[0]]:
                udp.sendto(
                    dumps([packet.append(wall_pos) for packet in pipe[data[0]]])
                    + b"||||",
                    address,
                )
                pipe[data[1]] = []
            else:
                udp.sendto(dumps([[":server:", wall_pos]]) + b"||||", address)


if __name__ == "__main__":
    multiprocessing.freeze_support()

    host = socket.gethostname()
    port = 9000
    udp_port = 9002
    team = []

    sock = socket.socket()
    try:
        sock.bind((host, port))
    except OSError:
        print(f"Port {port} is busy")

    sock.listen(1)
    print("Backend Active...")
    player_entry()
