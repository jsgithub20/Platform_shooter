import socket, json
from threading import Thread

server = socket.gethostbyname(socket.gethostname())
print(server)
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Server Started, waiting for connections... ")

def str_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def pos_str(tup):
    return str(tup[0]) + "," + str(tup[1])

def lst_del_item(list, del_item):
    for item in list:
        if item == del_item:
            list.remove(item)
    return list

def all_keys(dict):
    key_list = []
    for key in dict.keys():
        key_list.append(key)
    return key_list

pos = [(0, 0), (100, 100)]
player_opt = {"shooter": (0, 0), "chopper": (250, 250)}

def threaded_client(conn, player, addr):
    conn.sendall(json.dumps(player_opt).encode())
    # conn.sendall(",".join(all_keys(player_opt)).encode())
    player_selection = conn.recv(1024).decode()
    player_opt[player_selection] = "Not Available"
    # print(player_selection)
    reply = ""
    connected = True
    while connected:
        try:
            data = str_pos(conn.recv(1024).decode())
            pos[player] = data

            if not data:
                print(f"Disconnected from {addr}")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                # print("Received: ", data)
                # print("Sending : ", reply)

            conn.sendall(str.encode(pos_str(reply)))
        except:
            print(f"the client {addr} is disconnected")
            connected = False

    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    t = Thread(target=threaded_client, args=(conn, currentPlayer, addr))
    t.daemon = True
    t.start()

    currentPlayer += 1