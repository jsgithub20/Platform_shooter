import pygame as pg

pg.init()
screen = pg.display.set_mode((1024, 768))
pg.display.set_caption("my_pygame_learning")

# class XieSprite()



running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    pg.display.flip()

pg.quit()