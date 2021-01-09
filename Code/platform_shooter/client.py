import pygame
import json
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Client")

clientNumber = 0


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def str_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def pos_str(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    # startPos = str_pos(n.getPos())
    if n.player_role == "shooter":
        pygame.display.set_caption("Shooter_client: Red")
        me = Player(0,0,100,100,(255,0,0))
        they = Player(250,250,100,100,(0,255,0))
    elif n.player_role == "chopper":
        pygame.display.set_caption("Chopper_client: Green")
        me = Player(250,250,100,100,(0,255,0))
        they = Player(0,0,100,100,(255,0,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        they_pos = str_pos(n.send(pos_str((me.x, me.y))))
        they.x = they_pos[0]
        they.y = they_pos[1]
        they.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        me.move()
        redrawWindow(win, me, they)

main()