import socket
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

pos = [(0,0),(100,100)]

def threaded_client(conn, player, addr):
    # conn.send(str.encode(pos_str(pos[player])))
    reply = ""
    connected = True
    while connected:
        try:
            data = str_pos(conn.recv(2048).decode())
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