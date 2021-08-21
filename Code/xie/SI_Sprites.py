import pygame as pg
from settings import *


class Bullets(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 1

    def update(self):
        self.rect.x += self.speed

        if self.rect.right >= WIDTH:
            self.rect.y += (self.rect.h + 2)
            self.speed *= -1
        elif self.rect.left <= 0:
            self.rect.y += (self.rect.h + 2)
            self.speed *= -1


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT
        self.rect.x = WIDTH / 2
        self.speed = 2
        self.change_x = 0
        self.change_y = 0
        self.direction = "L"

    def update(self):
        self.rect.x += self.change_x

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

    def go_left(self):
        self.change_x = -self.speed
        self.direction = "L"

    def go_right(self):
        self.change_x = self.speed
        self.direction = "R"

    def stop(self):
        self.change_x = 0

    def go_home(self):
        self.rect.bottom = HEIGHT
        self.rect.x = WIDTH / 2


