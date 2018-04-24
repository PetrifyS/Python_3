import pygame as pg
import random
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.running = True
        self.score = 0
        self.bullet = 0
        self.font_name = pg.font.match_font('arial')
    
    def draw_text(self, text, size, color, x, y, align="topleft"):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.gold_img = pg.image.load(path.join(img_folder, GOLD_IMG)).convert_alpha()
        self.laser_img = pg.image.load(path.join(img_folder, LASER_IMG)).convert_alpha()
        self.meteor_images = []
        for i in range(1, 11):
            self.meteor_images.append(pg.image.load(path.join(img_folder, 'meteor{}.png'.format(i))).convert())
        self.player_img_d = pg.transform.scale(self.player_img, (15, 15))
        self.player_img_u = pg.transform.flip(self.player_img_d, False, True)
        self.player_img_r = pg.transform.rotate(self.player_img_d, 90)
        self.player_img_l = pg.transform.flip(self.player_img_r, True, False)
        self.laser_img_d = pg.transform.scale(self.laser_img, (3, 12))
        self.laser_img_u = pg.transform.flip(self.laser_img_d, False, True)
        self.laser_img_r = pg.transform.rotate(self.laser_img_d, 90)
        self.laser_img_l = pg.transform.flip(self.laser_img_r, True, False)
        self.gold_img = pg.transform.scale(self.gold_img, (15, 15))
                
                                        
    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.golds = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.lasers = pg.sprite.Group()
        self.ulasers = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.player = Player(self)
        self.gold = Gold(self)
        self.portal = Portal(self, 100, 100, 15, 15)
        self.portal2 = Portal(self, 300, 450, 15, 15)
        self.laser = Powerup(self, "laser")
        self.all_sprites.add(self.portal)
        self.portals.add(self.portal)
        self.all_sprites.add(self.portal2)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.gold)
        self.all_sprites.add(self.laser)
        self.ulasers.add(self.laser)
        self.golds.add(self.gold)
        self.num_of_mobs = 45
        if self.score >= 3:
            self.num_of_mobs = 55
        if self.score >= 9:
            self.num_of_mobs = 75
        for i in range(self.num_of_mobs):
            self.mob = Mob(self)
            self.mobs.add(self.mob)
            self.all_sprites.add(self.mob)
        for i in range(NUM_STARS):
            self.star = Star(self)
            self.stars.add(self.star)
            self.all_sprites.add(self.star)
            
        self.draw_debug = False
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        for hit in hits:
            self.score -= 1
            self.player.kill()
            self.new()
        # player hits gold
        hits = pg.sprite.collide_rect(self.player, self.gold)
        if hits:
            self.score += 1
            self.new()
        if self.score < 0:
            self.score = 0

        # player hits portal
        hits = pg.sprite.spritecollide(self.player, self.portals, False)
        for hit in hits:
            self.player.rect.center = self.portal2.rect.center
            self.player.pos = self.portal2.rect.center

        hits = pg.sprite.spritecollide(self.player, self.ulasers, False)
        for hit in hits:
            self.laser.kill()
            self.bullet += 1
            print(self.bullet)

        hits = pg.sprite.groupcollide(self.lasers, self.mobs, True, True)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def draw(self):
        # Game Loop - draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 18, WHITE, WIDTH / 2, 10)
        for sprite in self.all_sprites:
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, (sprite.rect), 1)
        for i in range(NUM_STARS - len(self.stars)):
            self.star = Star(self)
            self.stars.add(self.star)
            self.all_sprites.add(self.star)
            
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, YELLOW, WIDTH / 2, HEIGHT / 4)
        self.show_screen = 'main'
        self.buttons()
        pg.display.flip()
        self.wait_for_press()

    def show_in_screen(self):
        # game instructions
        self.screen.fill(BLACK)
        self.draw_text("Instructions", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use the Arrows keys to move", 24, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("If you have the bullet, you can shoot using the spacebar", 24, BLUE, WIDTH / 2, HEIGHT / 2 + 20)
        self.draw_text("Try to reach the gold, without hitting the asteriods", 24, BLUE, WIDTH / 2, HEIGHT / 2 + 40)
        self.draw_text("Good Luck!", 24, BLUE, WIDTH / 2, HEIGHT / 2 + 60)
        self.show_screen = 'instruction'      
        self.playbutton.rect.center = WIDTH / 2, HEIGHT * 7 / 8
        self.instbutton.kill()
        pg.display.flip()
        self.buttons.update()
        self.wait_for_press() 
         
    def show_go_screen(self):
        # game over/continue
        pass

    def buttons(self):
        self.buttons = pg.sprite.Group()
        self.playbutton = Button(self, WIDTH / 2, HEIGHT / 2, 115, 30, 'Play')
        self.instbutton = Button(self, WIDTH / 2, HEIGHT / 2 + 40, 115, 30, 'Instructions')
        self.buttons.add(self.playbutton)
        self.buttons.add(self.instbutton)
        self.buttons.draw(self.screen)
        self.playbutton.main_texts()
        
    def wait_for_press(self):
        self.waiting = True
        while self.waiting:
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(FPS)
            for self.event in pg.event.get():
                if self.event.type == pg.QUIT:
                    self.waiting = False
                    self.running = False
                self.buttons.update()
            
g = Game()
g.show_start_screen()
while g.running:
    g.show_go_screen()

pg.quit()
