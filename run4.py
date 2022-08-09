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
SCREEN_WIDTH = 1400 #1100,1400
SCREEN_HEIGHT = 800 #500,800


class Entity(Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = None
        self.rect = None
        self.base_image = None
        self.base_center = None
        self.heading = None
        self.speed = None
        self.msg = None
        self.name = name
        self.engageCommand = False
        self.perception_list = pg.sprite.Group()
        self.range_list = pg.sprite.Group()
        self.all_sprites_list = None
        self.bullet_list = None
        self.msg_box = None
        self.radar_mode = 0
        self.tracked_entity_id = None

    def set_radar_mode(self, mode, entity_id=None):
        if mode == 0: self.radar_mode = 0
        elif mode == 1: self.radar_mode = 1
        elif mode == 2:
            self.radar_mode = 2
            self.tracked_entity_id = entity_id
        else: print("Error: invalid radar mode, -command options: 0,1,2  -entity id")

    def get_radar_mode(self):
        return self.radar_mode

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
        bearing = math.degrees(rads)
        rbearing = bearing - self.heading
        if rbearing < -180: rbearing += 360
        elif rbearing > 180: rbearing -= 360
        # print("degs:{} h:{}  rb:{}".format(degs, self.heading, rbearing))
        return rbearing

    def get_bearing(self, entity):
        dx = entity.rect.x - self.rect.x
        dy = entity.rect.y - self.rect.y
        rads = math.atan2(dx, -dy)
        bearing = math.degrees(rads)
        return bearing

    def fire_to_entity(self, target_gid):
        for entity, gid in self.entity_list:
            if gid == target_gid: target = entity
        if target != 'skip' and target in self.perception_list and target in self.range_list:
            bullet = Bullet(self.rect.x, self.rect.y, target, self)
            self.all_sprites_list.add(bullet)
            self.bullet_list.add(bullet)
            print("fired to perceived target-",target_gid)
        else: print("target-"+str(target_gid)+"not perceived")

    def send_message(self, receiver, subject, text):
        msg = {}
        msg.update({'sender':self, 'receiver':receiver, 'subject':subject, 'text':text})
        self.msg_box.append(msg)

    def process_message(self, msg): # sender subject text
        sender = msg['sender']
        subject = msg['subject']
        text = msg['text']
        print(">>>>>>>>> {} send {} message to {}".format(sender.name,text,self.name))
        self.myEnemyGlobalID = subject.gid
        self.commanderID = sender.gid
        self.engageCommand = True


class Block(Entity):
    def __init__(self, name):
        super().__init__(name)
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
        self.heading = 0
        self.damage = 0
        self.entity_list = []

    def move(self):
        speed_vec = Vector2()
        speed_vec.from_polar((self.speed, self.heading-90))
        self.pos += speed_vec

    def update(self):
        super().update()
        self.rect.center = self.pos
        self.circle.rect_ = self.rect
        self.circle2.rect_ = self.rect

    def play(self):
        pass


class Circle(Sprite):
    def __init__(self, color, R, rect):
        super().__init__()
        self.image = pg.Surface((R, R), pg.SRCALPHA)
        pg.draw.circle(self.image, color, (R/2, R/2), R/2, 1)
        self.rect = self.image.get_rect()
        self.rect_ = rect

    def update(self):
        self.rect.center = self.rect_.center


class Player(Entity):
    def __init__(self, name):
        super().__init__(name)
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
        self.entity_list = []
        self.gid = random.randint(0,1000)
        self.heading = 0
        self.speed = 0
        self.damage = 0

    def update(self):
        super().update()

    def play(self):
        pass


class Bullet(Entity):
    def __init__(self, current_x, current_y, target, owner, name=None):
        super().__init__(name)
        self.image = pg.Surface([4, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = current_x
        self.rect.y = current_y
        self.pos = (self.rect.x, self.rect.y)
        self.speed = 1.05
        self.target = target
        self.gid = random.randint(0,1000)
        self.owner = owner

    def move(self):
        velocity_vec = Vector2()
        velocity_vec.from_polar((self.speed, self.get_bearing(self.target)-90))
        self.pos += velocity_vec

    def update(self):
        super().update()
        self.move()
        self.rect.center = self.pos
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.all_sprites_list = pg.sprite.Group()
        self.player_list = pg.sprite.Group()
        self.block_list = pg.sprite.Group()
        self.entity_list = pg.sprite.Group()
        self.bullet_list = pg.sprite.Group()
        self.block_number = 3
        self.msg_box = []
        self.player = Player('f'+str(0))
        self.player.msg_box = self.msg_box
        self.player_list.add(self.player)

        self.init_blocks()
        self.entity_list.add(self.player_list, self.block_list)
        self.all_sprites_list.add(self.player.circle, self.player.circle2, self.player)
        self.clock = pg.time.Clock()
        self.quit = False
        self.a = 0


        self.player.all_sprites_list = self.all_sprites_list
        self.player.bullet_list = self.bullet_list

    def init_blocks(self):
        for i in range(self.block_number):
            block = Block('h'+str(i))
            block.msg_box = self.msg_box
            block.all_sprites_list = self.all_sprites_list
            block.bullet_list = self.bullet_list
            block.entity_list.append((self.player, self.player.gid))
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
                    self.player.fire_to_entity(self.block_list.sprites()[0].gid)
                if event.key == pg.K_KP1 or event.key == pg.K_1:
                    self.player.fire_to_entity(self.block_list.sprites()[1].gid)
                if event.key == pg.K_KP2 or event.key == pg.K_2:
                    self.player.fire_to_entity(self.block_list.sprites()[2].gid)
                if event.key == pg.K_KP3 or event.key == pg.K_3:
                    self.block_list.sprites()[0].fire_to_block(self.player.gid)
                if event.key == pg.K_KP4 or event.key == pg.K_4:
                    self.block_list.sprites()[1].fire_to_block(self.player.gid)
                if event.key == pg.K_KP5 or event.key == pg.K_5:
                    self.block_list.sprites()[2].fire_to_block(self.player.gid)
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
                if event.key == pg.K_m:
                    self.player.send_message(receiver=self.block_list.sprites()[2], subject=self.block_list.sprites()[1], text='CLOSERADAR')
                    # self.send_message(sender=self.block_list.sprites()[2], receiver=self.block_list.sprites()[1], subject=self.player, text='ENGAGE')

            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                self.block_list.sprites()[0].pos = pos

    def handle_bullets(self):
        # Calculate mechanics for each bullet
        for bullet in self.bullet_list:
            hit_entity_list = pg.sprite.spritecollide(bullet, self.entity_list, False)
            for hit_entity in hit_entity_list:
                if bullet.owner.gid != hit_entity.gid:
                    self.bullet_list.remove(bullet)
                    self.block_list.remove(hit_entity)
                    self.all_sprites_list.remove(bullet, hit_entity, hit_entity.circle, hit_entity.circle2)
                    i = bullet.owner.entity_list.index((hit_entity, hit_entity.gid))
                    bullet.owner.entity_list[i] = ('skip', -1)
                    hit_entity.damage = 3

                if bullet.rect.y < -10:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)

            if bullet.target.damage == 3:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

    def handle_radar(self):
        # Calculate mechanics for each radar
        for entity in self.entity_list:
            entity.perception_list.empty()
            if entity.radar_mode == 1 or entity.radar_mode == 2:
                perception_list = pg.sprite.spritecollide(entity.circle, self.entity_list, False)
                if len(perception_list) > 0:
                    for perceived in perception_list:
                        if perceived.gid != entity.gid:
                            rb = entity.get_relativebearing(perceived)
                            if rb < 60 and rb > -60:
                                entity.perception_list.add(perceived)

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

    def handle_message(self):
        if len(self.msg_box) > 0:
            for msg in self.msg_box:
                receiver = msg['receiver']
                receiver.process_message(msg)
            self.msg_box.clear()

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
        self.a += 0.2
        if self.a >= 360:
            self.a = 0
        self.block_list.sprites()[0].set_heading(self.a)
        self.block_list.sprites()[0].set_speed(1)
        self.block_list.sprites()[0].move()
        self.player.set_radar_mode(1)
        # if len(self.bullet_list) > 0:
        #     self.bullet_list.sprites()[0].set_heading(60)
        self.all_sprites_list.update()
        self.handle_radar()
        self.handle_range()

        # print(self.player.perception_list)
        self.fire_bullet()
        self.handle_bullets()
        self.handle_message()
        self.render()
        # print(self.block_list)

    def quitter(self):
        self.quit = False
        for entity in self.player.entity_list:
            if entity[1] == -1: self.quit = True
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



