import pygame
import random
import math
import time
import numpy as np




class Game():
    def __init__(self):
        pygame.init()  # init (start)game
        pygame.display.set_caption("Red pills")  # title
        pygame.display.set_icon(pygame.image.load('neo.png'))

        self.player = Player()
        self.enemy = Enemy()
        self.bullets = []
        self.screen = pygame.display.set_mode((1000, 800,))
        self.clock = pygame.time.Clock()

    def step(self):
        self.screen.fill((0, 51, 102))
        self.screen.blit(self.player.img, (self.player.x, self.player.y))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        if len(self.bullets) > 0:
            for bullet  in self.bullets:
                bullet_rect = bullet.img.get_rect(center=bullet.pos)
                self.screen.blit(bullet.img, bullet_rect)

        pygame.display.update()

    def is_collided(self):

        is_collided = False
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                #is_collided = self.enemy.colliderect(bullet)
                #if is_collided:
                #    break
                distance = math.sqrt((self.enemy.x - bullet.pos[0]) ** 2 + (self.enemy.y - bullet.pos[1]) ** 2)
                if distance < 50:
                    is_collided = True
                    break
        return is_collided

class Bullet():
    def __init__(self):
        self.x = 510
        self.y = 375
        self.speed = 2
        self.pos = (self.x, self.y)

        self.initial_process()


    def initial_process(self):
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - self.x, my - self.y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.img = pygame.image.load('bullet.png')
        self.img = pygame.transform.rotate(self.img, angle)

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)


class Player():
    def __init__(self):
        self.img = pygame.image.load('star-wars.png')
        self.x = 475
        self.y = 350

class Enemy():
    def __init__(self):
        self.img = pygame.image.load('space-station.png')
        self.x = random.randint(0,900)
        self.y = random.randint(0,700)

    def approach(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        angle = math.atan2(dx, dy)
        mx = (math.sin(angle))*0.5
        my = math.cos((angle))*0.5
        self.x += mx
        self.y += my


game = Game()

running=True
while running:
    game.clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :  # close for press x
            running= False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet()
            game.bullets.append(bullet)

    for bullet in game.bullets[:]:
        bullet.update()
        if not game.screen.get_rect().collidepoint(bullet.pos):
            game.bullets.remove(bullet)

    game.enemy.approach(game.player)
    game.step()
    done = game.is_collided()
    if done:
        game.__init__()
