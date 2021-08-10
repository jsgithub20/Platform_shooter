import pygame as pg
import settings


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 1

    def update(self):
        self.rect.x += self.speed

        if self.rect.right >= settings.WIDTH:
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
        self.rect.bottom = settings.HEIGHT
        self.rect.x = settings.WIDTH / 2
        self.speed = 2
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.rect.x += self.change_x

        if self.rect.right >= settings.WIDTH:
            self.rect.right = settings.WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

    def go_left(self):
        self.change_x = -self.speed

    def go_right(self):
        self.change_x = self.speed

    def stop(self):
        self.change_x = 0

    def go_home(self):
        self.rect.bottom = settings.HEIGHT
        self.rect.x = settings.WIDTH / 2


