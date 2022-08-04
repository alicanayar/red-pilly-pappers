from .game import *


if __name__ == "__main__":
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
