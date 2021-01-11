import pygame as pg
from platform_shooter_settings import *
from platform_shooter_sprites import *
import sprite_player_correction


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.HWSURFACE)
        pg.display.set_caption(TITLE)
        # self.bg = pg.image.load("resources/platform/Tree_1024_768.png")
        # self.screen.blit(self.bg, (0, 0))
        self.clock = pg.time.Clock()
        self.winner = None
        self.running = True

    def new(self):
        # fps display
        self.fps_txt = DrawText(self.screen, 10, WHITE, 25, 0)

        # start a new game
        self.bullets = []

        # Create the self.player
        self.player_shooter = Player()
        self.player_shooter.hit_limit = 60
        self.player_shooter.score_text = DrawText(self.screen, 20, WHITE, 200, 10)

        self.player_chopper = sprite_player_correction.Player()
        self.player_chopper.hit_limit = 10
        # self.player_chopper.image.fill(WHITE)
        self.player_chopper.score_text = DrawText(self.screen, 20, WHITE, 800, 10)

        # Create all the levels
        self.level_list = []
        self.level_list.append(Level_01(self.player_shooter))
        self.level_list.append(Level_01(self.player_chopper))

        # Set the current level
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        self.active_sprite_list = pg.sprite.Group()
        self.bullet_sprite_grp = pg.sprite.Group()

        self.player_shooter.level = self.current_level
        self.player_shooter.rect.x = 200
        self.player_shooter.rect.y = 0

        self.player_chopper.level = self.current_level
        self.player_chopper.rect.x = 600
        self.player_chopper.rect.y = 200

        self.active_sprite_list.add(self.player_shooter, self.player_chopper)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.player_shooter.go_left()
                if event.key == pg.K_RIGHT:
                    self.player_shooter.go_right()
                if event.key == pg.K_UP:
                    self.player_shooter.jump()
                if event.key == pg.K_SPACE:
                    if self.player_shooter.loaded > 0:
                        self.player_shooter.reload_timer = pg.time.get_ticks()
                        self.player_shooter.loaded -= 1
                        if self.player_shooter.direction == 'l':
                            bullet = Bullet(self.player_shooter.rect.x, self.player_shooter.rect.y, 'l', SCREEN_WIDTH)
                            bullet.level = self.current_level
                            self.player_shooter.attack_flg = 1
                        else:
                            bullet = Bullet(self.player_shooter.rect.x, self.player_shooter.rect.y, 'r', SCREEN_WIDTH)
                            bullet.level = self.current_level
                            self.player_shooter.attack_flg = 1
                        self.bullets.append(bullet)
                        self.bullet_sprite_grp.add(bullet)
                    else:
                        if pg.time.get_ticks() - self.player_shooter.reload_timer >= 4000:
                            self.player_shooter.loaded = 5

                # player_chopper controls
                if event.key == pg.K_a:
                    self.player_chopper.go_left()
                if event.key == pg.K_d:
                    self.player_chopper.go_right()
                if event.key == pg.K_w:
                    self.player_chopper.jump()
                if event.key == pg.K_c:
                    self.player_chopper.chop()
                    self.player_chopper.image_idx = 0

            if event.type == pg.KEYUP:
                # player_shooter controls
                if event.key == pg.K_LEFT and self.player_shooter.change_x < 0:
                    self.player_shooter.stop()
                if event.key == pg.K_RIGHT and self.player_shooter.change_x > 0:
                    self.player_shooter.stop()

                # player_chopper controls
                if event.key == pg.K_a and self.player_chopper.change_x < 0:
                    self.player_chopper.stop()
                if event.key == pg.K_d and self.player_chopper.change_x > 0:
                    self.player_chopper.stop()

    def update(self):
        # Game Loop - Update
        # Update the player.
        self.active_sprite_list.update()
        self.bullet_sprite_grp.update()
        if self.player_chopper in self.active_sprite_list:
            bullet_hit_chopper = pg.sprite.spritecollideany(self.player_chopper, self.bullet_sprite_grp)
            if bullet_hit_chopper:
                bullet_hit_chopper.live_flag = 0
                self.player_chopper.hit_flag = 1
                self.player_chopper.hit_count += 1

                if self.player_chopper.hit_count == self.player_chopper.hit_limit:
                    self.active_sprite_list.remove(self.player_chopper)
                    self.playing = False
                    self.winner = "Shooter"

            if pg.sprite.collide_rect(self.player_shooter, self.player_chopper):
                if self.player_shooter.hit_flag == 0 and self.player_chopper.chop_flag == 1:
                    self.player_shooter.hit_flag = 1
                    self.player_shooter.hit_count += 1
                    if self.player_shooter.hit_count > self.player_shooter.hit_limit:
                        self.active_sprite_list.remove(self.player_shooter)
                        self.playing = False
                        self.winner = "Chopper"
                elif self.player_shooter.hit_flag == 1 and self.player_chopper.chop_flag == 0:
                    self.player_shooter.hit_flag = 0

        if self.bullets:
            for bullet in self.bullets:
                if bullet.live_flag == 0:
                    self.bullet_sprite_grp.remove(bullet)
                    self.bullets.remove(bullet)

        # Update items in the level
        self.current_level.update()

    def draw(self):
        # Game Loop - draw
        self.current_level.draw(self.screen)
        self.active_sprite_list.draw(self.screen)
        self.bullet_sprite_grp.draw(self.screen)
        self.player_chopper.score_text.draw("Chopper Hit: {}/{}".format(self.player_chopper.hit_count,
                                                                         self.player_chopper.hit_limit))
        self.player_shooter.score_text.draw("Shooter Hit: {}/{}".format(self.player_shooter.hit_count,
                                                                         self.player_shooter.hit_limit))
        self.fps_txt.draw("fps: {}".format(str(int(self.clock.get_fps()))))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        background = pg.image.load("resources/gui/Window_06.png").convert_alpha()
        title = DrawText(self.screen, 50, GREEN, 350, 25)
        name = DrawText(self.screen, 40, WHITE, 200, 300)
        server_IP = DrawText(self.screen, 40, WHITE, 200, 350)
        server_Port = DrawText(self.screen, 40, WHITE, 200, 400)
        settings_btn = Buttons("resources/gui/settings.png", 100, 500)
        start_btn = Buttons("resources/gui/right.png", 400, 500)
        credit_btn = Buttons("resources/gui/credit.png", 700, 500)
        btn_sprites = pg.sprite.Group()
        btn_sprites.add(settings_btn, start_btn, credit_btn)
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    btn_sprites.update(pg.mouse.get_pos())
                    for button in btn_sprites:
                        pass

            self.screen.blit(background, (0, 0))
            btn_sprites.draw(self.screen)
            title.draw("My Game")
            name.draw("Name: ")
            server_IP.draw("Server IP: ")
            server_Port.draw("Server Port: ")
            pg.display.flip()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        # pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        # pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        game_over_text = DrawText(self.screen, 60, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        game_over_text.draw("GAME OVER")
        winner_text = DrawText(self.screen, 50, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        winner_text.draw("{} WINS!".format(self.winner))
        # self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        press_key_text = DrawText(self.screen, 40, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        press_key_text.draw("Press a key to play again")
        # if self.score > self.highscore:
        #     self.highscore = self.score
        #     self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        #     with open(path.join(self.dir, HS_FILE), 'w') as f:
        #         f.write(str(self.score))
        # else:
        #     self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        pg.time.wait(2000)
        self.wait_for_key()
        # pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()