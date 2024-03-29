import csv
import os

import pygame as pg
import pygame.freetype as ft
from random import randint, choice

from typing import Optional

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
VER = "Splat Generator V0.2"
FPS = 60
WIDTH = 1024
HEIGHT = 768
FONT_PATH = "resources/fonts/"

# sound: Optional['pygame_menu.sound.Sound'] = None
# surface: Optional['pg.Surface'] = pg.image.load("resources\gui\Window_06.png")
# main_menu: Optional['pygame_menu.Menu'] = None


class DrawText(pg.sprite.Sprite):
    def __init__(self, word_lst, font_lst, x, y):
        super().__init__()
        self.word_lst = word_lst
        self.text = choice(self.word_lst)
        self.fg_color = [(237, 105, 27), (166, 214, 201), (250, 185, 10)]
        self.bg_color = (0, 0, 0)
        self.font = ft.Font(FONT_PATH + font_lst[randint(0, (len(font_lst)-1))], 80)
        self.rendered_ft = self.font.render(self.text, fgcolor=self.fg_color[randint(0, 2)],
                                            rotation=randint(-5, 5))
        self.image = self.rendered_ft[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shadow = None

    def update(self) -> None:
        pass

    def add_shadow(self):
        self.shadow = self.font.render(self.text, (100, 100, 100))[0]
        self.shadow.blit(self.image, (-2, -2))
        self.image = self.shadow

    def get_lst(self):
        self.word_lst.remove(self.text)
        return self.word_lst


class Game:
    def __init__(self):
        pg.init()
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.NOFRAME)
        # self.screen = pg.display.set_mode(flags=pg.NOFRAME | pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF)
        self.screen_size = pg.display.get_window_size()
        self.screen_w = self.screen_size[0]
        self.screen_h = self.screen_size[1]
        self.screen_centerx = int(self.screen_w / 2)
        self.screen_centery = int(self.screen_h / 2)
        self.splat_font = ft.Font(FONT_PATH + "earwig factory rg.ttf", 80)
        self.any_key_font = ft.SysFont("calibri", 30)
        self.amy_font = ft.SysFont("calibri", 15)
        self.font_lst = os.listdir(FONT_PATH)
        self.txt_grp = pg.sprite.Group()
        self.x, self.y, self.w, self.h = 0, 0, 0, 0
        self.file_saved_flg = False
        self.file_saved_cnt = 1
        self.file_saved_name = ""
        self.word_lst = None

    def new(self):
        self.word_lst = self.read_csv("words.csv")
        self.load_screen()

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pg.K_SPACE:
                    self.word_lst = self.read_csv("words.csv")
                    if self.file_saved_flg:
                        self.file_saved_flg = False
                    self.load_screen()
                if event.key == pg.K_s:
                    self.file_saved_name = "splat_screen_" + str(self.file_saved_cnt) + ".png"
                    pg.image.save(self.screen, self.file_saved_name)
                    self.file_saved_flg = True
                    self.file_saved_cnt += 1

    def update(self):
        self.txt_grp.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.txt_grp.draw(self.screen)
        self.amy_font.render_to(self.screen, (self.screen_w - 250, self.screen_h - 50), VER + ". by Amy Yao")

        if self.file_saved_flg:
            self.any_key_font.render_to(self.screen, (self.screen_centerx-150, self.screen_centery+50),
                                        "screen saved to: " + self.file_saved_name, bgcolor=(200, 100, 100))

        pg.display.flip()

    def start_screen(self):
        running = True
        while running and self.running:
            self.clock.tick(FPS)
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                    else:
                        running = False

            self.screen.fill((255, 255, 255))
            self.splat_font.render_to(self.screen, (self.screen_centerx-330, self.screen_centery-150), "SPLAT Generator", fgcolor=(237, 105, 27))
            self.any_key_font.render_to(self.screen, (self.screen_centerx-150, self.screen_centery+50), "Press Any Key To Continue", fgcolor=(166, 214, 201))
            self.amy_font.render_to(self.screen, (self.screen_w-250, self.screen_h-50), VER + ". by Amy Yao")

            pg.display.flip()

    def end_screen(self):
        running = True
        while running:
            self.clock.tick(FPS)
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    running = False
                    self.running = False

            self.screen.fill((255, 255, 255))
            self.splat_font.render_to(self.screen, (self.screen_centerx-500, self.screen_centery-150), "Enjoy, Bye For Now!", fgcolor=(237, 105, 27))
            self.any_key_font.render_to(self.screen, (self.screen_centerx-150, self.screen_centery+50), "Press Any Key To Exit", fgcolor=(166, 214, 201))
            self.amy_font.render_to(self.screen, (self.screen_w-250, self.screen_h-50), VER + ". by Amy Yao")

            pg.display.flip()

    def load_screen(self):
        if not self.running:
            return
        self.txt_grp.empty()
        self.x, self.y, self.w, self.h = 50, 50, 0, 0
        word_lst = self.word_lst
        for i in range(len(self.word_lst)):
            text = DrawText(word_lst, self.font_lst, self.x, self.y)
            word_lst = text.get_lst()
            if self.x + text.rect.w + 50 <= self.screen_w:
                text.rect.x = self.x
                text.rect.y = self.y
                self.x = self.x + text.rect.w + 100
                self.txt_grp.add(text)
            else:
                if self.y + text.rect.h + 100 <= self.screen_h:
                    self.x = randint(50, 150)
                    text.rect.x = self.x
                    self.x = self.x + text.rect.w + 50
                    text.rect.y = self.y + text.rect.h + 20
                    self.y = text.rect.y
                    self.txt_grp.add(text)
                else:
                    break

    def read_csv(self, file_name, dict=0):
        result = None
        if dict == 0:
            try:
                with open(file_name, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    result = []
                    for item in reader:
                        result.append(item[0])
            except FileNotFoundError:
                self.no_file_screen(file_name)
        elif dict == 1:
            try:
                with open(file_name, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for item in reader:
                        print(item)
            except FileNotFoundError:
                self.no_file_screen(file_name)
        return result

    def no_file_screen(self, file_name):
        while self.running:
            self.clock.tick(FPS)
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                    self.playing = False
                if event.type == pg.KEYDOWN:
                    self.running = False
                    self.playing = False

            self.screen.fill((255, 255, 255))
            self.any_key_font.render_to(self.screen, (self.screen_centerx-200, self.screen_centery-50),
                                        f"File {file_name} is not found.", fgcolor=(166, 214, 201))
            self.any_key_font.render_to(self.screen, (self.screen_centerx-150, self.screen_centery+50),
                                        "Press Any Key To Exit", fgcolor=(166, 214, 201))
            self.amy_font.render_to(self.screen, (self.screen_w-250, self.screen_h-50), VER + ". by Amy Yao")

            pg.display.flip()


g = Game()
g.start_screen()
while g.running:
    g.new()
    g.run()
    # g.end_screen()

pg.quit()