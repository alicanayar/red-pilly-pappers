import pygame as pg
from pygame.sprite import Sprite
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

class Block(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()


class Circle(Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pg.Surface((400, 400))
        self.image.fill((255, 255, 255))
        pg.draw.circle(self.image, (255, 0, 0), (200, 200), 200, 2)
        self.rect = self.image.get_rect()
        self.rect_ = rect

    def update(self):
        self.rect.center = self.rect_.center

class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([20, 20])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # pg.draw.circle(self.image, BLACK, (self.rect.x, self.rect.y), 10)
        # self.i = 1
        # pg.draw.arc(self.image, (0,255,255),(25,25,45,45),0+(self.i*math.pi)/180,math.pi/6 +(self.i*math.pi)/180,10)
        self.circle = Circle(self.rect)
        self.radar_mode = 0
        self.tracked_entity_id = None

    def set_radar_mode(self, cmd, entity_id=None):
        if cmd == 0:
            self.radar_mode = 0
        elif cmd == 1:
            self.radar_mode = 1
        elif cmd == 2:
            self.radar_mode = 2
            self.tracked_entity_id = entity_id
        else:
            print("Error: invalid radar mode, -command options: 0,1,2  -entity id")

    def get_radar_mode(self):
        return self.radar_mode

    def update(self):
        super().update()




class Bullet(Sprite):
    def __init__(self, current_x, current_y, target_x, target_y):
        super().__init__()
        self.image = pg.Surface([4, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = current_x
        self.rect.y = current_y
        self.x = current_x
        self.y = current_y

        x_distance = target_x - current_x
        y_distance = target_y - current_y
        heading = math.atan2(y_distance, x_distance)

        velocity = 5
        self.dx = math.cos(heading) * velocity
        self.dy = math.sin(heading) * velocity

    def update(self):
        self.y += self.dy
        self.x += self.dx
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.all_sprites_list = pg.sprite.Group()
        self.block_list = pg.sprite.Group()
        self.bullet_list = pg.sprite.Group()
        self.block_number = 3
        self.init_blocks()

        self.player = Player()
        self.all_sprites_list.add(self.player.circle, self.player)
        self.clock = pg.time.Clock()
        self.player.rect.x = SCREEN_WIDTH / 2
        self.player.rect.y = SCREEN_HEIGHT / 2

    def init_blocks(self):
        for i in range(self.block_number):
            block = Block()
            # Set a random location for the block
            block.rect.x = random.randrange(SCREEN_WIDTH)
            block.rect.y = random.randrange(SCREEN_HEIGHT - 50)
            # Add the block to the list of objects
            self.block_list.add(block)
            self.all_sprites_list.add(block)

    def reset(self):
        self.__init__()

    def listen_events(self):
        # --- Event Processing
        quit = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                # Create the bullet based on where we are, and where we want to go.
                if len(self.block_list.sprites()) > 0:
                    target = self.block_list.sprites()[0]
                    bullet = Bullet(self.player.rect.x, self.player.rect.y, target.rect.x, target.rect.y)
                    # Add the bullet to the lists
                    self.all_sprites_list.add(bullet)
                    self.bullet_list.add(bullet)
        return quit

    def handle_bullets(self):
        # Calculate mechanics for each bullet
        for bullet in self.bullet_list:
            # See if it hit a block
            block_hit_list = pg.sprite.spritecollide(bullet, self.block_list, True)
            # For each block hit, remove the bullet and add to the score
            if len(block_hit_list) > 0:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

    def render(self):
        self.screen.fill(WHITE)
        self.all_sprites_list.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)

    def execute(self):
        quit = self.listen_events()
        # --- Game logic
        # Call the update() method on all the sprites
        self.all_sprites_list.update()
        self.handle_bullets()
        self.render()
        return quit


if __name__ == "__main__":
    game = Game()
    episodes = 5
    for episode in range(episodes):
        game.reset()
        quit = False
        while not quit:
            quit = game.execute()
    pg.quit()


""" moveCircle.py
    create a blue circle sprite and have it
    follow the mouse"""

import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

class Circle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (255, 0, 0), (25, 25), 25, 2)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

def main():
    pygame.display.set_caption("move the circle with the mouse")

    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    circle = Circle()
    allSprites = pygame.sprite.Group(circle)

    #hide mouse
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

    #return mouse
    pygame.mouse.set_visible(True)

# if __name__ == "__main__":
#     main()
