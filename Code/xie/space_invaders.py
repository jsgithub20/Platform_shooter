import pygame as pg


class Game:
    def __init__(self):
        pass
        self.running = True

    def new(self):
        pass
        self.restart()

    def restart(self):
        pass
        self.run()

    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def start_screen(self):
        pass

    def game_end(self):
        pass


g = Game()
g.start_screen()
while g.running:
    g.new()
    g.game_end()

pg.quit()