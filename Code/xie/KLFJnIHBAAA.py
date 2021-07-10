import pygame as pg
import random as rand

pg.init()
screen = pg.display.set_mode((800, 768))
pg.display.set_caption("FEUIDJRFGVB 9QISJHBVFERU38IFKMREHJG8WFODKITVYGUI$TY(UIb")


class XiClass(pg.sprite.Sprite):
    def __init__(self, file_name):
        super().__init__()
        self.image = pg.image.load(file_name)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


Chaotic = pg.sprite.Group()
xio = XiClass("PEACE WAS NEVER AN OPTION smol.png")
Chaotic.add(xio)

running = True
while running:
    ASDf = rand.randint(5, 20)
    OI = rand.randint(175, 255)
    FG = rand.randint(175, 255)
    AAAA = rand.randint(175, 255)
    randx = rand.randint(-75, 780)
    randy = rand.randint(-75, 748)
    print("A"*ASDf)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    screen.fill((0, 0, OI))
    xio.rect.x = randx
    xio.rect.y = randy
    Chaotic.update()
    Chaotic.draw(screen)
    pg.display.update()

    screen.fill((0, FG, 0))
    xio.rect.x = randx
    xio.rect.y = randy
    Chaotic.update()
    Chaotic.draw(screen)
    pg.display.update()

    screen.fill((0, 0, 0))
    xio.rect.x = randx
    xio.rect.y = randy
    Chaotic.update()
    Chaotic.draw(screen)
    pg.display.update()

    screen.fill((AAAA, 0, 0))
    xio.rect.x = randx
    xio.rect.y = randy
    Chaotic.update()
    Chaotic.draw(screen)
    pg.display.update()

pg.quit()
