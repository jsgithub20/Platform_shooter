import socket, json


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.3.10"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_pos = (0, 0)
        self.player_opt = ()
        self.player_role = ""
        self.connect()

    #
    # def getPos(self):
    #     return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.player_opt = self.client.recv(1024).decode()
            player_dict = json.loads(self.player_opt)
            for key, value in player_dict.items():
                print(key+":"+str(value))
            selection = input("Please choose your role: ")
            print(f"Your selection is: {selection}")
            self.client.sendall(selection.encode())
            self.player_role = selection
            self.player_pos = player_dict[selection]
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(data.encode())
            return self.client.recv(10).decode()
        except socket.error as e:
            print(e)