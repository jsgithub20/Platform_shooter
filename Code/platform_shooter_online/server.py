import socket
from threading import Thread
import pickle
from game_state import GameState

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(f"Server Address: {SERVER}:{PORT}")
ADDR = (SERVER, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(ADDR)
except socket.error as e:
    print(e)

s.listen()
print("Server Started, waiting for connections... ")

games = {}
id_cnt = 0


def threaded_client(conn, player, game_id):
    global id_cnt
    conn.sendall(str(player).encode)  # send player number

    while True:
        try:
            data = conn.recv(4096)
            obj = pickle.loads(data)  # receive the client object

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass
    id_cnt -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_cnt += 1
    player = 0
    game_id = (id_cnt - 1)//2
    if id_cnt % 2 == 1:
        games[game_id] = GameState(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        player = 1

    t = Thread(target=threaded_client, args=(conn, player, game_id))
    t.daemon = True
    t.start()