import pygame as pg

WIDTH = 1024
HEIGHT = 768

# images for player_shooter
# Run animation for the RIGHT
run_R = [pg.image.load("resources/shooter/Run__000.png"), pg.image.load("resources/shooter/Run__001.png"),
         pg.image.load("resources/shooter/Run__002.png"), pg.image.load("resources/shooter/Run__003.png"),
         pg.image.load("resources/shooter/Run__004.png"), pg.image.load("resources/shooter/Run__005.png"),
         pg.image.load("resources/shooter/Run__006.png"), pg.image.load("resources/shooter/Run__007.png"),
         pg.image.load("resources/shooter/Run__008.png"), pg.image.load("resources/shooter/Run__009.png")]

# Run animation for the LEFT
run_L = [pg.transform.flip(sprite, True, False) for sprite in run_R]

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("pygame basicssssss")


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w, h))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MovingPlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.change_y = 1
        self.boundary_top = 100
        self.boundary_bottom = 600

    def update(self):
        self.rect.y += self.change_y

        if self.rect.top < self.boundary_top or self.rect.bottom > self.boundary_bottom:
            self.change_y *= -1


class XieClass(pg.sprite.Sprite):
    def __init__(self, file_name, file_num=0):
        super().__init__()
        # self.image = pg.image.load(file_name).convert_alpha()
        self.image = run_R[0]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = 400
        self.file_num = file_num
        self.speed = 2
        self.img_idx = 0
        self.change_x = 0
        self.change_y = 1

    def update(self):
        if self.file_num == 1:
            self.rect.x += self.change_x
            if self.rect.left >= WIDTH:
                self.rect.right = 0
            elif self.rect.right <= 0:
                self.rect.left = WIDTH

            self.calc_grav()

            self.rect.y += self.change_y

            if self.rect.y > HEIGHT - self.rect.h:
                self.rect.y = HEIGHT - self.rect.h

        if self.change_x < 0:
            self.image = self.chg_frame(run_L)
        elif self.change_x > 0:
            self.image = self.chg_frame(run_R)

    def chg_frame(self, img_lst):
        if self.img_idx + 1 == len(img_lst) * 2:
            self.img_idx = 0
        else:
            self.img_idx += 1
        # print(self.img_idx // 2)
        return img_lst[self.img_idx // 2]

    def go_left(self):
        self.change_x = -self.speed

    def go_right(self):
        self.change_x = self.speed

    def stop(self):
        self.change_x = 0

    def calc_grav(self):
        self.change_y += 0.35

    def jump(self):
        self.change_y = -10


my_grp = pg.sprite.Group()
xies = XieClass("idle_1.png", 1)
block_1 = Platform(WIDTH/2, HEIGHT/2, 75, 20)
block_2 = Platform(WIDTH*2/3, HEIGHT*2/3, 75, 20)
block_m1 = MovingPlatform(WIDTH*1/3, HEIGHT/2, 75, 20)
plat_grp = pg.sprite.Group()
plat_grp.add(block_1, block_2, block_m1)
my_grp.add(xies)

clock = pg.time.Clock()

running = True
while running:
    clock.tick(60)
    # clock.tick_busy_loop(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_LEFT:
                xies.go_left()
            if event.key == pg.K_RIGHT:
                xies.go_right()
            if event.key == pg.K_UP:
                xies.jump()

        if event.type == pg.KEYUP:
            xies.stop()

    # now = xies.rect.x0
    xies.update()
    plat_grp.update()

    hit_blocks = pg.sprite.spritecollide(xies, plat_grp, False)
    if hit_blocks:
        if xies.change_y > 0:
            xies.rect.bottom = hit_blocks[0].rect.top
        elif xies.change_y < 0:
            xies.rect.top = hit_blocks[0].rect.bottom

        xies.change_y = 0
    # print(xies.rect.x - now)
    screen.fill((100, 200, 100))
    my_grp.draw(screen)
    plat_grp.draw(screen)
    pg.display.update()

pg.quit()
