import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 255)
SCREEN_WIDTH = 1400 #1100
SCREEN_HEIGHT = 800 #500


class Entity(Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        # pg.draw.circle(self.image, RED, (10, 10), 10)
        # pg.draw.rect(self.image, RED, (0, 10, 20, 20))
        self.rect = None
        self.base_image = None
        self.base_center = None
        self.heading = None
        self.speed = None

    def set_heading(self, heading):
        heading = heading % 360
        self.heading = heading
        if heading > 0: heading = 360 - heading
        else: heading = heading*(-1)
        self.image = pg.transform.rotate(self.base_image, heading)
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_speed(self, speed):
        self.speed = speed

    def get_relativebearing(self, entity):
        dx = entity.rect.x - self.rect.x
        dy = entity.rect.y - self.rect.y
        rads = math.atan2(dx, -dy)
        degs = math.degrees(rads)
        rb = degs - self.heading
        if rb < -180: rb += 360
        elif rb > 180: rb -= 360
        # print("degs:{} h:{}  rb:{}".format(degs, self.heading, rb))
        return rb

class Block(Entity):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([20, 30], pg.SRCALPHA)
        pg.draw.circle(self.image, RED, (10, 10), 10)
        pg.draw.rect(self.image, RED, (0, 10, 20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = random.randrange(SCREEN_HEIGHT - 50)
        self.pos = (self.rect.x, self.rect.y)
        self.base_image = self.image
        self.base_center = self.rect.center
        self.circle = Circle(RED, 300, self.rect)
        self.circle2 = Circle(RED, 100, self.rect)
        self.gid = random.randint(0,1000)
        self.perception_list = pg.sprite.Group()
        self.range_list = pg.sprite.Group()
        self.heading = 0

    def move(self):
        velocity_vec = Vector2()
        velocity_vec.from_polar((self.speed, self.heading-90))
        self.pos += velocity_vec

    def update(self):
        super().update()
        self.rect.center = self.pos
        self.circle.rect_ = self.rect
        self.circle2.rect_ = self.rect


class Circle(Sprite):
    def __init__(self, color, R, rect):
        super().__init__()
        self.image = pg.Surface((R, R), pg.SRCALPHA)
        # self.image.fill(WHITE)
        pg.draw.circle(self.image, color, (R/2, R/2), R/2, 1)
        self.rect = self.image.get_rect()
        self.rect_ = rect

    def update(self):
        self.rect.center = self.rect_.center


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([20, 30], pg.SRCALPHA)
        pg.draw.circle(self.image, BLUE, (10, 10), 10)
        pg.draw.rect(self.image, BLUE, (0, 10, 20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT / 2
        self.pos = (self.rect.x, self.rect.y)
        self.base_image = self.image
        self.base_center = self.rect.center

        self.circle = Circle(BLUE, 400, self.rect)
        self.circle2 = Circle(BLUE, 300, self.rect)
        self.radar_mode = 0
        self.tracked_entity_id = None
        self.perception_list = pg.sprite.Group()
        self.range_list = pg.sprite.Group()
        self.entity_list = []
        self.gid = random.randint(0,1000)
        self.heading = 0
        self.speed = 0

    def set_radar_mode(self, mode, entity_id=None):
        if mode == 0:
            self.radar_mode = 0
        elif mode == 1:
            self.radar_mode = 1
        elif mode == 2:
            self.radar_mode = 2
            self.tracked_entity_id = entity_id
        else:
            print("Error: invalid radar mode, -command options: 0,1,2  -entity id")

    def get_radar_mode(self):
        return self.radar_mode

    def update(self):
        super().update()


class Bullet(Entity):
    def __init__(self, current_x, current_y, target, gid):
        super().__init__()
        self.image = pg.Surface([4, 10])
        self.image.fill(BLACK)
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.base_center = self.rect.center
        self.rect.x = current_x
        self.rect.y = current_y
        self.pos = (self.rect.x, self.rect.y)
        self.x = current_x
        self.y = current_y
        self.speed = 1.1
        self.target = target
        self.target_pos = (self.target.rect.x, self.target.rect.y)
        self.guide()
        self.gid = random.randint(0,1000)
        self.owner_gid = gid

    # def set_heading(self, heading):
    #     heading = heading % 360
    #     self.heading = heading
    #     if heading > 0: heading = 360 - heading
    #     else: heading = heading*(-1)
    #     self.image = pg.transform.rotate(self.base_image, heading)
    #     self.rect = self.image.get_rect(center=self.rect.center)

    def guide(self):
        self.target_pos = (self.target.rect.x, self.target.rect.y)
        x_distance = self.target_pos[0] - self.x
        y_distance = self.target_pos[1] - self.y
        heading = math.atan2(y_distance, x_distance)
        return heading
        # print(heading)

        # self.dx = math.cos(heading) * self.speed
        # self.dy = math.sin(heading) * self.speed

    def move(self):
        heading = self.guide()
        velocity_vec = Vector2()
        velocity_vec.from_polar((self.speed, heading))
        self.pos += velocity_vec

    def update(self):
        # self.rect.center = self.pos
        # self.guide()
        super().update()
        self.move()
        self.rect.center = self.pos
        # self.y += self.dy
        # self.x += self.dx
        # self.rect.y = int(self.y)
        # self.rect.x = int(self.x)

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.all_sprites_list = pg.sprite.Group()
        self.player_list = pg.sprite.Group()
        self.block_list = pg.sprite.Group()
        self.bullet_list = pg.sprite.Group()
        self.block_number = 3
        self.player = Player()
        self.player_list.add(self.player)

        self.init_blocks()
        self.all_sprites_list.add(self.player.circle, self.player.circle2, self.player)
        self.clock = pg.time.Clock()
        self.quit = False
        self.a = 0

    def init_blocks(self):
        for i in range(self.block_number):
            block = Block()
            self.block_list.add(block)
            self.all_sprites_list.add(block, block.circle, block.circle2)
            self.player.entity_list.append((block, block.gid))

    def reset(self):
        self.__init__()

    def listen_events(self):
        # --- Event Processing
        self.quit = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True

    def fire_bullet(self):
        # --- Event Processing
        self.quit = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_KP0 or event.key == pg.K_0:
                    self.fire_to_target(0)
                if event.key == pg.K_KP1 or event.key == pg.K_1:
                    self.fire_to_target(1)
                if event.key == pg.K_KP2 or event.key == pg.K_2:
                    self.fire_to_target(2)
                if event.key == pg.K_KP3 or event.key == pg.K_3:
                    self.fire_to_player(3)
                if event.key == pg.K_KP4 or event.key == pg.K_4:
                    self.fire_to_player(4)
                if event.key == pg.K_KP5 or event.key == pg.K_5:
                    self.fire_to_player(5)
                if event.key == pg.K_RIGHT:
                    self.player.set_heading(30)
                if event.key == pg.K_LEFT:
                    self.player.set_heading(270)
                if event.key == pg.K_DOWN:
                    self.block_list.sprites()[0].set_heading(-450)
                if event.key == pg.K_UP:
                    self.block_list.sprites()[0].set_heading(50)
                if event.key == pg.K_b:
                    # rb = self.player.get_relativebearing(self.block_list.sprites()[0])
                    rb = self.block_list.sprites()[0].get_relativebearing(self.player)
                    print("rb:", rb)
                if event.key == pg.K_w:
                    self.block_list.sprites()[0].move(0,-5)
                if event.key == pg.K_s:
                    self.block_list.sprites()[0].move(0,5)
                if event.key == pg.K_a:
                    self.block_list.sprites()[0].move(-5,0)
                if event.key == pg.K_d:
                    self.block_list.sprites()[0].move(5,0)
                if event.key == pg.K_m:
                    self.block_list.sprites()[0].move(5,self.block_list.sprites()[0].heading)

            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                self.block_list.sprites()[0].pos = pos

    def fire_to_target(self, target_no):
        target = self.player.entity_list[target_no][0]
        if target != 'skip' and target in self.player.perception_list and target in self.player.range_list:
            bullet = Bullet(self.player.rect.x, self.player.rect.y, target, self.player.gid)
            self.all_sprites_list.add(bullet)
            self.bullet_list.add(bullet)
            print("fired to perceived target-",target_no)
        else:
            print("target-"+str(target_no)+"not perceived")

    def fire_to_player(self, striker_no):
        striker = self.player.entity_list[striker_no-3][0]
        if striker != 'skip' and len(self.player_list)!=0:
            if self.player in striker.perception_list and self.player in striker.range_list:
                bullet = Bullet(striker.rect.x, striker.rect.y, self.player.rect.x, self.player.rect.y, striker.gid)
                self.all_sprites_list.add(bullet)
                self.bullet_list.add(bullet)
                print("fired striker-",striker_no-3)
        else:
            print("striker-"+str(striker_no-3)+" destroyed")

    def handle_bullets(self):
        # Calculate mechanics for each bullet
        for bullet in self.bullet_list:
            if bullet.owner_gid == self.player.gid:
                # See if it hit a block
                block_hit_list = pg.sprite.spritecollide(bullet, self.block_list, True)
                # For each block hit, remove the bullet and add to the score
                for block in block_hit_list:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet, block.circle, block.circle2)
                    i = self.player.entity_list.index((block, block.gid))
                    self.player.entity_list[i] = ('skip', -1)
                # Remove the bullet if it flies up off the screen
                if bullet.rect.y < -10:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
            else:
                # See if it hit a block
                block_hit_list = pg.sprite.spritecollide(bullet, self.player_list, True)
                # For each block hit, remove the bullet and add to the score
                for block in block_hit_list:
                    self.quit = True
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                    # i = self.player.entity_list.index((block, block.gid))
                    # self.player.entity_list[i] = ('skip', -1)
                # Remove the bullet if it flies up off the screen
                if bullet.rect.y < -10:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)

    def handle_block_bullets(self):
        # Calculate mechanics for each bullet
        for bullet in self.bullet_list:
            # See if it hit a block
            block_hit_list = pg.sprite.spritecollide(bullet, self.player_list, False)
            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
                # i = self.player.entity_list.index((block, block.gid))
                # self.player.entity_list[i] = ('skip', -1)
            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

    def handle_radar(self):
        self.player.perception_list.empty()
        perception_list = pg.sprite.spritecollide(self.player.circle, self.block_list, False)
        if len(perception_list) > 0:
            for perceived in perception_list:
                rb = self.player.get_relativebearing(perceived)
                if rb < 60 and rb > -60:
                    self.player.perception_list.add(perceived)

        for block in self.block_list:
            block.perception_list.empty()
            perception_list = pg.sprite.spritecollide(block.circle, self.player_list, False)
            if len(perception_list) > 0:
                for perceived in perception_list:
                    rb = block.get_relativebearing(perceived)
                    if rb < 60 and rb > -60:
                        block.perception_list.add(perceived)

    def handle_range(self):
        self.player.range_list.empty()
        range_list = pg.sprite.spritecollide(self.player.circle2, self.block_list, False)
        if len(range_list) > 0:
            for ranged in range_list:
                self.player.range_list.add(ranged)

        for block in self.block_list:
            block.range_list.empty()
            range_list = pg.sprite.spritecollide(block.circle2, self.player_list, False)
            if len(range_list) > 0:
                for ranged in range_list:
                    block.range_list.add(ranged)

    def render(self):
        self.screen.fill(WHITE)
        self.all_sprites_list.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)

    def execute(self):
        # quit = self.listen_events()
        # --- Game logic
        # Call the update() method on all the sprites
        # self.listen_events()
        self.a += 1
        if self.a >= 360:
            self.a = 0
        self.block_list.sprites()[0].set_heading(self.a)
        self.block_list.sprites()[0].set_speed(5)
        self.block_list.sprites()[0].move()
        # if len(self.bullet_list) > 0:
        #     self.bullet_list.sprites()[0].set_heading(60)
        self.all_sprites_list.update()
        self.handle_radar()
        self.handle_range()
        # print(self.player.perception_list)
        self.fire_bullet()
        self.handle_bullets()
        self.render()
        # print(self.player.entity_list)
        # print("--",self.block_list.sprites())
        # for sprit in self.block_list.sprites():
        #     print(sprit.gid)
        # self.quitter()

    def quitter(self):
        self.quit = False
        for entity in self.player.entity_list:
            if entity[1] == -1:
                self.quit = True
            else:
                self.quit = False
                break



if __name__ == "__main__":
    game = Game()
    episodes = 5
    for episode in range(episodes):
        game.reset()
        while not game.quit:
            game.execute()
    pg.quit()



