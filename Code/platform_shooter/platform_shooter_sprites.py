import pygame as pg
from platform_shooter_settings import *

# images for player_shooter
# Run animation for the RIGHT
run_R = [pg.image.load("resources/shooter/Run__000.png"), pg.image.load("resources/shooter/Run__001.png"),
         pg.image.load("resources/shooter/Run__002.png"), pg.image.load("resources/shooter/Run__003.png"),
         pg.image.load("resources/shooter/Run__004.png"), pg.image.load("resources/shooter/Run__005.png"),
         pg.image.load("resources/shooter/Run__006.png"), pg.image.load("resources/shooter/Run__007.png"),
         pg.image.load("resources/shooter/Run__008.png"), pg.image.load("resources/shooter/Run__009.png")]

# Run animation for the LEFT
run_L = [pg.transform.flip(sprite, True, False) for sprite in run_R]

# Attack animation for the RIGHT
attack_R = [pg.image.load("resources/shooter/Throw__000.png"), pg.image.load("resources/shooter/Throw__001.png"),
            pg.image.load("resources/shooter/Throw__002.png"), pg.image.load("resources/shooter/Throw__003.png"),
            pg.image.load("resources/shooter/Throw__004.png"), pg.image.load("resources/shooter/Throw__005.png"),
            pg.image.load("resources/shooter/Throw__006.png"), pg.image.load("resources/shooter/Throw__007.png"),
            pg.image.load("resources/shooter/Throw__008.png"), pg.image.load("resources/shooter/Throw__009.png")]

# Attack animation for the LEFT
attack_L = [pg.transform.flip(sprite, True, False) for sprite in attack_R]

# tiles of the platforms
blocks = [pg.image.load("resources/platform/13.png"),
          pg.image.load("resources/platform/14.png"),
          pg.image.load("resources/platform/15.png")]

long_block = pg.Surface([210, 40], pg.SRCALPHA)
long_block.blit(blocks[0], (0, 0))
long_block.blit(blocks[1], (70, 0))
long_block.blit(blocks[2], (140, 0))


class DrawText:
    def __init__(self, screen, size, color, x, y):
        self.screen = screen
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.font = pg.font.Font("resources/You Blockhead.ttf", self.size)
        # self.font = pg.font.SysFont(None, self.size)

    def draw(self, text):
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x, self.y)
        self.screen.blit(text_surface, text_rect)


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, screen_width):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("resources/shooter/spear_head.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = direction
        self.screen_width = screen_width
        self.live_flag = 1
        self.speed = 10
        self.loop_count = 0
        self.level = None
        if self.direction == 'l':
            self.speed = -self.speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = self.screen_width
            self.loop_count += 1
        if self.rect.x > self.screen_width:
            self.rect.x = 0
            self.loop_count += 1
        if self.loop_count == 2:
            self.live_flag = 0
        if pg.sprite.spritecollide(self, self.level.platform_list, False):
            self.live_flag = 0


class Player(pg.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image_idx = 0
        self.image = run_R[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        self.speed = 6

        # List of sprites we can bump against
        self.level = None

        self.direction = 'r'

        self.hit_count = 0
        self.hit_flag = 0
        self.jump_count = 0
        self.hit_limit = 0
        self.score_text = None
        self.loaded = 5
        self.reload_timer = 0
        self.attack_flg = 0

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        if self.attack_flg == 1:
            self.chg_frame(attack_L)
        else:
            if self.change_x < 0:
                self.chg_frame(run_L)
            elif self.change_x > 0:
                self.chg_frame(run_R)

        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.jump_count = 0
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        # If the player gets near the right side, shift the world left (-x)
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0

        # If the player gets near the left side, shift the world right (+x)
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            # self.change_y = 0
            self.jump_count = 0
            # self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.rect.y =  0

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # check whether it's double jump
        self.jump_count += 1

        # If it is ok to jump, set our speed upwards
        # if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT or self.jump_count <= 2:
        if self.jump_count <= 1:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        self.direction = 'l'

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = 'r'

    def stop(self):
        """ Called when the user lets off the keyboard. """
        if self.change_x > 0:
            self.direction = 'r'
        elif self.change_x < 0:
            self.direction = 'l'
        self.change_x = 0

    def chg_frame(self, img_list):
        if self.attack_flg == 1:
            if self.direction == 'l':
                img_list = attack_L
            elif self.direction == "r":
                img_list = attack_R
        if self.image_idx + 1 == len(img_list):
            self.image_idx = 0
            if self.attack_flg == 1:
                self.attack_flg = 0
        else:
            self.image_idx += 1
        self.image = img_list[self.image_idx]


class Platform(pg.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, pos_x, pos_y):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
        self.image = long_block

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Level:
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()
        self.player = player

        # Background image
        # self.background = pg.image.load("resources/platform/Tree_1024_768.png").convert_alpha()
        self.background = pg.image.load("resources/platform/angry_owl.png").convert_alpha()

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.blit(self.background, (0, 0))
        # screen.fill(LIGHT_BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)


        # Array with width, height, x, and y of platform
        level = [[500, 500],
                 [200, 400],
                 [700, 300],
                 [200, 200],
                 [100, 100],
                 [600, 100],
                 [100, 500],
                 [50, 650],
                 [600, 650],
                 [0, 300],
                 [924, 500],
                 [400, 300],
                 [440, 270]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.player = self.player
            self.platform_list.add(block)
