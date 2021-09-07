import pygame as pg
from settings import *
import SI_Sprites
from pythonWordArt import pyWordArt



class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.background = pg.image.load("background.png")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.blit(self.background, (0, 0))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = 1

        self.level_0_enemy = 10
        self.level_0_speed = 1
        self.level_1_enemy = 10
        self.level_1_speed = 2

        self.enemy_grp = None
        self.player = None
        self.player_grp = None
        self.bullet_grp = None

    def new(self):
        self.enemy_grp = pg.sprite.Group()
        self.player = SI_Sprites.Player()
        self.player.go_home()
        self.player_grp = pg.sprite.GroupSingle(self.player)
        self.bullet_grp = pg.sprite.Group()

        for i in range(self.level_0_enemy):
            enemy = SI_Sprites.Enemy()
            enemy.rect.x = (WIDTH / self.level_0_enemy) * i
            enemy.rect.y = 10
            self.enemy_grp.add(enemy)

        w = pyWordArt()
        w.transparentBackground = True
        w.noOpenGL = False
        w.WordArt("Text here", w.Styles["rainbow"], "100")
        w.toFile("w_test")
        print("file saved.")

        self.run()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.go_left()
                if event.key == pg.K_RIGHT:
                    self.player.go_right()
                if event.key == pg.K_SPACE:
                    bullet = SI_Sprites.Bullets(self.player.rect.x, self.player.rect.y)
                    self.bullet_grp.add(bullet)

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and self.player.direction == "L":
                    self.player.stop()
                elif event.key == pg.K_RIGHT and self.player.direction == "R":
                    self.player.stop()

    def update(self):
        self.enemy_grp.update()
        self.player_grp.update()
        self.bullet_grp.update()

        pg.sprite.groupcollide(self.bullet_grp, self.enemy_grp, True, True)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.enemy_grp.draw(self.screen)
        self.player_grp.draw(self.screen)
        self.bullet_grp.draw(self.screen)
        pg.display.update()

    def start_screen(self):
        pass

    def game_end(self):
        pass


g = Game()
# g.start_screen()
while g.playing:
    g.new()
    # g.game_end()

pg.quit()