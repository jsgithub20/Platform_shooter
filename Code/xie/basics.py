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


class DrawText(pg.sprite.Sprite):
    def __init__(self, text, pos_x, pos_y):
        super().__init__()
        self.my_font = pg.font.SysFont("arial", 30)
        self.text = text
        self.image = self.my_font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.image = self.my_font.render(self.text, True, (255, 255, 255))


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, screen_width):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.screen_width = screen_width
        self.speed = 10
        self.live_flag = 1
        self.loop_count = 0
        if direction == "l":
            self.speed = -self.speed

    def update(self):
        self.rect.x += self.speed

        if self.rect.x > self.screen_width:
            self.rect.x = 0
            self.loop_count += 1
        elif self.rect.x < 0:
            self.rect.x = self.screen_width
            self.loop_count += 1

        if self.loop_count >= 2:
            self.live_flag = 0


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
        self.my_grp = None  # block_m1.my_grp = my_grp

    def update(self):
        self.rect.y += self.change_y

        hit_blocks = pg.sprite.spritecollide(self, self.my_grp, False)
        if hit_blocks:
            for hit in hit_blocks:
                if self.change_y > 0:
                    hit.rect.top = self.rect.bottom
                elif self.change_y < 0:
                    hit.rect.bottom = self.rect.top

        if self.rect.top < self.boundary_top or self.rect.bottom > self.boundary_bottom:
            self.change_y *= -1


class XieClass(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = run_R[0]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = 400
        self.speed = 2
        self.img_idx = 0
        self.change_x = 0
        self.change_y = 1
        self.plat_grp = None
        self.direction = "r"
        self.score = 0

    def update(self):
        self.calc_grav()
        self.rect.y += self.change_y

        if self.rect.y > HEIGHT - self.rect.h:
            self.rect.y = HEIGHT - self.rect.h

        self.collision_y()

        self.rect.x += self.change_x
        if self.rect.left >= WIDTH:
            self.rect.right = 0
        elif self.rect.right <= 0:
            self.rect.left = WIDTH

        if self.change_x < 0:
            self.direction = "l"
            self.image = self.chg_frame(run_L)
        elif self.change_x > 0:
            self.direction = "r"
            self.image = self.chg_frame(run_R)

        self.collision_x()

    def collision_y(self):
        hit_blocks = pg.sprite.spritecollide(self, self.plat_grp, False)
        if hit_blocks:
            if self.change_y > 0:
                self.rect.bottom = hit_blocks[0].rect.top
            elif self.change_y < 0:
                self.rect.top = hit_blocks[0].rect.bottom

            self.change_y = 0

    def collision_x(self):
        hit_blocks = pg.sprite.spritecollide(self, self.plat_grp, False)
        if hit_blocks:
            if self.change_x > 0:
                self.rect.right = hit_blocks[0].rect.left
            elif self.change_x < 0:
                self.rect.left = hit_blocks[0].rect.right

            self.change_x = 0

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
        if self.change_y == 0:
            self.change_y = 1
        self.change_y += 0.35

    def jump(self):
        self.change_y = -10


my_grp = pg.sprite.Group()
xies = XieClass()
poirot = XieClass()
poirot.rect.x = 400
my_grp.add(xies, poirot)

block_1 = Platform(WIDTH/2, HEIGHT/2, 75, 20)
block_2 = Platform(WIDTH*2/3, HEIGHT*2/3, 75, 20)
block_3 = Platform(WIDTH/4, 720, 75, 20)
block_m1 = MovingPlatform(WIDTH/3, HEIGHT/2, 75, 20)
block_m1.my_grp = my_grp
plat_grp = pg.sprite.Group()
plat_grp.add(block_1, block_2, block_3, block_m1)

xies.plat_grp = plat_grp
poirot.plat_grp = plat_grp

bullet_grp = pg.sprite.Group()
bullet_lst = []

fps_txt = DrawText("0", 0, 0)

txt_grp = pg.sprite.GroupSingle(fps_txt)

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
            if event.key == pg.K_SPACE:
                bullet = Bullet(xies.rect.x, xies.rect.y, xies.direction, WIDTH)
                bullet_grp.add(bullet)
                bullet_lst.append(bullet)
            if event.key == pg.K_a:
                poirot.go_left()
            if event.key == pg.K_d:
                poirot.go_right()
            if event.key == pg.K_w:
                poirot.jump()

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                xies.stop()
            if event.key == pg.K_a or event.key == pg.K_d:
                poirot.stop()

    fps_txt.text = f"FPS: {clock.get_fps():4.1f}, FPS = Frame Per Second"
    my_grp.update()
    plat_grp.update()
    bullet_grp.update()
    txt_grp.update()

    bullet_hit_poirot = pg.sprite.spritecollideany(poirot, bullet_grp)
    if bullet_hit_poirot:
        bullet_hit_poirot.live_flag = 0
        xies.score += 1
        print(f"xies scores! total = {xies.score}")

    if bullet_lst:
        for bullet in bullet_lst:
            if not bullet.live_flag:
                bullet_lst.remove(bullet)
                bullet_grp.remove(bullet)

    if pg.sprite.collide_rect(xies, poirot):
        poirot.score += 1
        print(f"poirot scores! total = {poirot.score}")

    # print(xies.rect.x - now)
    screen.fill((100, 200, 100))
    my_grp.draw(screen)
    plat_grp.draw(screen)
    bullet_grp.draw(screen)
    txt_grp.draw(screen)
    pg.display.update()

pg.quit()
