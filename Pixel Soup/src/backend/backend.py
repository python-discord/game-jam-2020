import socket
from threading import Thread
from random import randint
from pickle import loads, dumps
from time import sleep


host = socket.gethostname()
port = 9000
udp_port = 9002
create_room = {}

sock = socket.socket()
try:
    sock.bind((host, port))
except OSError:
    print(f"Port {port} is busy")

sock.listen(1)


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

    # receives connection parameters from player
    data = conn.recv(1024)
    data = (data.decode("utf-8")).split(",,")

    if len(data) == 3:
        if data[0] == "create":
            # to check if the username is already in use
            if data[1] in create_room.keys():
                conn.send(b"Rename")
            else:
                create_room[data[1]] = [[conn, data[2]]]
                conn.send(b"Done")

                team_count = 1

                # looping to detect new teammates
                room_section = create_room[data[1]]
                while True:
                    sleep(1)
                    if len(room_section) > 1:
                        if team_count == 1:
                            conn.send(f"Team,,{room_section[1][1]}".encode())
                            team_count += 1

                        elif len(room_section) == 3:
                            conn.send(f"Team,,{room_section[2][1]}".encode())
                            room_section[1][0].send(
                                f"Team,,{room_section[2][1]}".encode()
                            )

                            while True:
                                try:
                                    team_udp_port = udp_port
                                    udp_port += 1

                                    udp = socket.socket(
                                        socket.AF_INET, socket.SOCK_DGRAM
                                    )
                                    udp.bind((host, team_udp_port))

                                    udp.close()
                                    room_password = randint(1000, 9999)
                                    for player in room_section:
                                        player[0].send(
                                            f"Start,,{team_udp_port},"
                                            f",{room_password},"
                                            f",{room_section[0][1]} "
                                            f"{room_section[1][1]} "
                                            f"{room_section[2][1]}".encode()
                                        )

                                    # creates a thread for players room
                                    room = Thread(
                                        target=game_room,
                                        args=[
                                            team_udp_port,
                                            room_password,
                                            [
                                                room_section[0][1],
                                                room_section[1][1],
                                                room_section[2][1],
                                            ],
                                        ],
                                    )
                                    room.start()
                                    return
                                except OSError:
                                    continue

        elif data[0] == "join":
            # checks if room's name exists
            if data[1] in create_room.keys():
                room = create_room[data[1]]
                player_count = len(room)

                if player_count == 3:
                    conn.send(b"Full")

                else:
                    room.append([conn, data[2]])
                    conn.send(b"Joined")

                for i in range(player_count):
                    waiting_player = room[i]
                    conn.send(f"Team,,{waiting_player[1]}".encode())

            else:
                conn.send(b"Missing")


def game_room(team_port: int, password: int, players: list) -> None:
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((host, team_port))

    pipe = {players[0]: [], players[1]: [], players[2]: []}
    sent_player = []
    wall_pos = 400

    while True:
        data, address = udp.recvfrom(1024)
        data = data.split(b"||||")

        if len(data) > 1:
            data = loads(data[0])

            if int(data[0]) == password:
                if data[1] in sent_player:
                    wall_pos = randint(10, 600)
                    sent_player = [data[1]]
                else:
                    sent_player.append(data[1])

                # pasting game data in pipe
                for player in pipe.keys():
                    if len(data) > 2:
                        if data[1] != player:
                            if len(pipe[player]) == 2:
                                pipe[player].pop(0)
                            pipe[player].append(data[1:])

                # checking if viable data is available to be sent
                if pipe.get(data[1]):
                    udp.sendto(
                        dumps([packet.append(wall_pos) for packet in pipe[data[1]]])
                        + b"||||",
                        address,
                    )
                    pipe[data[1]] = []
                else:
                    udp.sendto(dumps([[":server:", wall_pos]]) + b"||||", address)


if __name__ == "__main__":
    print("Backend Active...")
    player_entry()
