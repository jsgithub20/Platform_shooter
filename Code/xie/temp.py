class Test:
    def __init__(self, x):
        self.x = x


t_lst = []
t = Test(1)
t_lst.append(t)
t = Test(2)
t_lst.append(t)

for t in t_lst:
    print(t.x)
