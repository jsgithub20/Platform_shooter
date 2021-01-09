player_opt = {"shooter": (0, 0), "chopper": (250, 250)}
# string = str(player_opt)
# print(dict(string))
# print(key for key, value in player_opt.items())
# print((key, value) for key, value in player_opt.items())
player_opt["shooter"] = 1
for key, value in player_opt.items():
    print(key+":"+str(value))

