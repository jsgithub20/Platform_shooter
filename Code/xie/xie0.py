import pygame
import sys
import random

# The follow upper case variables are constants

PURPLE = (255, 1, 255)
TESTING_COLOR = (100, 200, 40)
WINDOW_W = 800
WINDOW_H = 600

# The following portion is class/function definitions


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, up_key, down_key):
        pygame.sprite.Sprite.__init__(self)
        self.up_key = up_key
        self.down_key = down_key
        self.key_state = None
        self.image = pygame.Surface((10, 80))
        self.image.fill(TESTING_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centery = WINDOW_H/2
        self.rect.left = pos_x
        self.dy = 0

    def update(self):
        self.key_state = pygame.key.get_pressed()
        if self.key_state[self.up_key]:
            self.dy = -3
        if self.key_state[self.down_key]:
            self.dy = 3
        self.rect.top += self.dy
        self.dy = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_H:
            self.rect.bottom = WINDOW_H


class ScoreThingy:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.score_font = pygame.font.Font("You Blockhead.ttf", 25)

    def update(self, player):
        if player == 1:
            self.score1 += 1
        elif player == 2:
            self.score2 += 1

    def draw(self, window):
        score1_sur = self.score_font.render(("Player1: " + str(self.score1)), True, (25, 220, 190))
        score2_sur = self.score_font.render(("Player2: " + str(self.score2)), True, (25, 220, 190))
        window.fill((0, 0, 0))
        window.blit(score1_sur, (WINDOW_W/6, 6*WINDOW_H/7))
        window.blit(score2_sur, (455, 6*WINDOW_H/7))


class PooferCircle:
    def __init__(self):
        self.num = 0
        self.window = None

    def draw_circle(self, num_circles):
        self.num = num_circles
        pos_x = random.randint(0, WINDOW_W)
        pos_y = random.randint(0, WINDOW_H)
        radii = random.randint(1, 6)
        pygame.draw.circle(game_window, (255, 255, 255), (pos_x, pos_y), radii)

    def clear_circle(self, game_win):
        self.window = game_win
        self.window.fill((0, 0, 0))


class SpriteTest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = None
        # self.sprite_list = []
        self.sprite_list_r = []
        self.sprite_list_l = []
        self.image = None
        self.rect = None
        self.direction = 'right'
        self.direction_flag = None
        self.collision_flag = None
        self.dx = 2
        self.frame_number = 0
        self.crash = pygame.mixer.Sound("Crash.wav")
        self.crash.set_volume(0.3)

    def load(self, file_name, width, height, columns):
        self.sprite_sheet = pygame.image.load(file_name)
        for i in range(columns):
            self.sprite_list_r.append(self.sprite_sheet.subsurface(pygame.Rect(i*width, 0, width, height)))
            self.sprite_list_l.append(pygame.transform.flip(self.sprite_list_r[i], 1, 0))
        self.image = self.sprite_list_r[0]
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 250

    def update(self):
        if self.frame_number == len(self.sprite_list_r) -1:
            self.frame_number = 0
        elif self.frame_number < len(self.sprite_list_r) -1:
            self.frame_number += 1

        if self.direction == "right":
            self.image = self.sprite_list_r[self.frame_number]
            if self.collision_flag == "right":
                self.collision_flag = None
                self.crash.play()
                self.dx = 0
            self.rect.x += self.dx
            self.dx = 2
            self.direction_flag = "right"
        elif self.direction == "left":
            self.image = self.sprite_list_l[self.frame_number]
            if self.collision_flag == "left":
                self.collision_flag = None
                self.crash.play()
                self.dx = 0
            self.rect.x -= self.dx
            self.dx = 2
            self.direction_flag = "left"
        elif self.direction is None:
            if self.direction_flag == "right":
                self.image = self.sprite_list_r[0]
            elif self.direction_flag == "left":
                self.image = self.sprite_list_l[0]
        self.direction = None

    #
    # def draw(self, game_window):
    #     game_window.blit(self.image, (200, 250))


def draw_circle(one):
    pressed = one
    pos_x = random.randint(0, WINDOW_W)
    pos_y = random.randint(0, WINDOW_H)
    radii = random.randint(1, 6)
    pygame.draw.circle(game_window, (255, 255, 255), (pos_x, pos_y), radii)
    return pressed, "means '1' is pressed"

# for name in pygame.font.get_fonts():
#     print(name)

# The following portion is to initialize pygame environment


pygame.init()

game_window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("xie.py")

# game_font = pygame.font.SysFont("YouBlockhead", 60)
game_font = pygame.font.Font("You Blockhead.ttf", 30)
game_txt = game_font.render("Le animal de hoot", 1, (255, 85, 1))

xie_clock = pygame.time.Clock()
fps = 30
num_circle = 0

pygame.mixer.music.load("background.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# Create instances with the class defined above

xie_circle = PooferCircle()
xie_score = ScoreThingy()
walking_xie = SpriteTest()
walking_xie.load('owl_ground_70percent_walking.png', 89.58, 81, 12)

xie_player1 = Player(786, pygame.K_UP, pygame.K_DOWN)
xie_player2 = Player(4, pygame.K_w, pygame.K_s)
all_sprites = pygame.sprite.Group()
all_sprites.add(xie_player1, xie_player2)
walking_grp_sgl = pygame.sprite.GroupSingle()
walking_grp_sgl.add(walking_xie)


# The following is the game loop


while True:
    xie_clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        exit()
    if key[pygame.K_1]:
        num_circle = num_circle + 1
        xie_circle.draw_circle(num_circle)
        print(xie_circle.num)
    if key[pygame.K_p]:
        xie_circle.clear_circle(game_window)
        num_circle = 0
    if key[pygame.K_d]:
        xie_score.update(1)
    if key[pygame.K_RIGHT]:
        walking_xie.direction = "right"
        # xie_score.update(2)
    if key[pygame.K_LEFT]:
        walking_xie.direction = "left"

    all_sprites.update()
    walking_grp_sgl.update()
    collision = pygame.sprite.spritecollideany(walking_xie, all_sprites)
    if collision == xie_player2:
        walking_xie.collision_flag = "left"
    if collision == xie_player1:
        walking_xie.collision_flag = "right"
    xie_score.draw(game_window)
    all_sprites.draw(game_window)
    pygame.draw.line(game_window, PURPLE, (WINDOW_W/2, 0), (WINDOW_W/2, WINDOW_H), 6)
    pygame.draw.line(game_window, (255, 255, 1), (0, WINDOW_H/3), (WINDOW_W, WINDOW_H/4), 12)
    pygame.draw.circle(game_window, (1, 149, 255), (int(WINDOW_W/2), int(WINDOW_H/2)), 251, 1)
    game_window.blit(game_txt, (0, WINDOW_H/7))
    walking_grp_sgl.draw(game_window)
    # walking_xie.draw(game_window)

    pygame.display.update()


# tuple_stuff = (1, 2, 3, 'f')
# lst_stuff = [1, 2, 3, 'f']
#
# lst_stuff[3] = 'y'
# print(lst_stuff[3])
#
# lst_stuff[0] = 3
#
# for item in lst_stuff:
#     if item == 3:
#         print(item)
#
# dict = {'a': 1, 'b': 2, 'c': 3, 'd': 0}
# if dict['c']:
#     print(dict['a'])


