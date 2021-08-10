import pygame as pg
import settings
import SI_Sprites

WIDTH = 1024
HEIGHT = 768
TITLE = "SPACE INVADERS"


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.background = pg.image.load("background.png")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
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

    def new(self):
        self.enemy_grp = pg.sprite.Group()
        self.player = SI_Sprites.Player()
        self.player.go_home()
        self.player_grp = pg.sprite.GroupSingle(self.player)

        for i in range(self.level_0_enemy):
            enemy = SI_Sprites.Enemy()
            enemy.rect.x = (settings.WIDTH / self.level_0_enemy) * i
            enemy.rect.y = 10
            self.enemy_grp.add(enemy)

        self.run()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(settings.FPS)
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

    def update(self):
        self.enemy_grp.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.enemy_grp.draw(self.screen)

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