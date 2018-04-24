# Sprite classes for platform game
import pygame as pg
import math
import random
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.player_img_d
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (15, 15)
        self.pos = vec(15, 15)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.image = self.game.player_img_l
            self.acc.x = -PLAYER_ACC
        elif keys[pg.K_RIGHT]:
            self.image = self.game.player_img_r
            self.acc.x = PLAYER_ACC
        elif keys[pg.K_UP]:
            self.image = self.game.player_img_u
            self.acc.y = -PLAYER_ACC
        elif keys[pg.K_DOWN]:
            self.image = self.game.player_img_d
            self.acc.y = PLAYER_ACC
        if keys[pg.K_SPACE] and self.game.bullet > 0:
            self.game.bullet -= 1
            self.shoot()
        
        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos

    def shoot(self):
        self.laser = Laser(self.game, self.rect.centerx, self.rect.centery)
        self.game.all_sprites.add(self.laser)
        self.game.lasers.add(self.laser)

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = random.choice(self.game.meteor_images)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        if self.image == self.game.meteor_images[6] or self.image == self.game.meteor_images[7] or self.image == self.game.meteor_images[8] or self.image == self.game.meteor_images[9]:
            scale = random.randrange(15, 30) / 100
        elif self.image == self.game.meteor_images[0] or self.image == self.game.meteor_images[1]:
            scale = random.randrange(35, 50) / 100
        else:
            scale = random.randrange(55, 70) / 100  
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale),
                                                     int(self.rect.height * scale)))
        self.rect = self.image.get_rect()

        # The "center" the sprite will orbit
        self.center_x = WIDTH / 2
        self.center_y = HEIGHT / 2
        # Current angle in radians
        self.angle = random.random() * 2 * math.pi
        # How far away from the center to orbit, in pixels
        self.radius = random.randrange(60, 300)
        # How fast to orbit, in radians per frame
        if self.game.score >= 6 and self.game.score <= 11:
            self.speed = 0.01
        elif self.game.score >= 12:
            self.speed = 0.02
        else:
            self.speed = 0.008

    def update(self):
        """ Update the ball's position. """
        # Calculate a new x, y
        self.rect.x = self.radius * math.sin(self.angle) + self.center_x
        self.rect.y = self.radius * math.cos(self.angle) + self.center_y

        # Increase the angle in prep for the next round.
        self.angle += self.speed

class Gold(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.gold_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)

class Button(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, action):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(LIGHT_BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.action = action

    def update(self):
        self.cur = pg.mouse.get_pos()
        if self.rect.left < self.cur[0] < self.rect.right and self.rect.top < self.cur[1] < self.rect.bottom:
            self.image.fill(LIGHT_BLUE)
            self.game.buttons.draw(self.game.screen)
            if self.game.show_screen == 'main':
                self.main_texts()
            elif self.game.show_screen == 'instruction':
                self.inst_texts()
            if self.game.event.type == pg.MOUSEBUTTONUP:
                if self.action == 'Play':
                    self.game.waiting = False
                    self.game.new()
                if self.action == 'Instructions':
                    self.game.waiting = False
                    self.game.show_in_screen()
                    
        else:
            self.image.fill(BLUE)
            self.game.buttons.draw(self.game.screen)
            if self.game.show_screen == 'main':
                self.main_texts()
            elif self.game.show_screen == 'instruction':
                self.inst_texts()
                
    def main_texts(self):
        self.game.draw_text("Play", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.game.draw_text("Instructions", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

    def inst_texts(self):
        self.game.draw_text("Play", 22, WHITE, WIDTH / 2, HEIGHT * 7 / 8)

class Portal(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, power):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.power = power
        if self.power == "laser":
            self.image = self.game.laser_img_u
        else:
            self.image = None
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, 700)
        self.rect.centery = random.randrange(0, 700)
        

class Laser(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.laser_img_d
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y        
        if self.game.player.image == self.game.player_img_l:
            self.image = self.game.laser_img_l
            self.speedx = -20
            self.speedy = 0
        elif self.game.player.image == self.game.player_img_r:
            self.image = self.game.laser_img_r
            self.speedx = 20
            self.speedy = 0
        elif self.game.player.image == self.game.player_img_u:
            self.image = self.game.laser_img_u
            self.speedy = -20
            self.speedx = 0
        elif self.game.player.image == self.game.player_img_d:
            self.image = self.game.laser_img_d
            self.speedy = 20
            self.speedx = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        
    def update(self):
        self.rect.centery += self.speedy
        self.rect.centerx += self.speedx
        
        if self.rect.bottom < 0:
             self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()

class Star(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((1, 1))
        self.image.fill(STAR_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.dir = random.randrange(360)
        self.speed = random.random()*.6 + .4
        self.vel = [math.sin(self.dir) * self.speed, math.cos(self.dir) * self.speed]
        self.steps = random.randint(0, 320) * .9
        
    def update(self):
        self.rect.centerx += self.vel[0] *self.steps
        self.rect.centery += self.vel[1] * self.steps
        if not 0 <= self.rect.centerx <= WIDTH or not 0 <= self.rect.centery <= HEIGHT:
            self.kill()
        else:
            self.vel[0] = self.vel[0] * 1.05
            self.vel[1] = self.vel[1] * 1.05
        
        
    
        
    

