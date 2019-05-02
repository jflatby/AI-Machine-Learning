import pygame
from player import Player
from food import Food

class Game:
    def __init__(self, network):
        pygame.init()
        self.display = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface(self.display.get_size())
        self.background.fill((0, 0, 0))

        self.food = Food()
        self.player = Player(self.food)

        self.network = network

        self.sprite_list = pygame.sprite.Group()
        self.sprite_list.add(self.player)
        self.sprite_list.add(self.food)

    def simple_loop(self):
        clock = pygame.time.Clock()
        dead = False

        while not dead:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.print_results()
                    exit()

            # self.network.advance(self.player, self.food)
            if pygame.sprite.collide_rect(self.player, self.food):
                self.player.points += 1
                self.player.got_point = True
                self.food.respawn()
            else:
                self.player.got_point = False

            if self.player.position.x < 0 or self.player.position.y < 0 or self.player.position.x > 800 or self.player.position.y > 600:
                self.player.die()
                dead = True

            self.network.advance(self.player, self.food)

            ## Draw, update screen, tick fps
            self.display.blit(self.background, (0, 0))
            self.sprite_list.draw(self.display)
            pygame.display.update()
            clock.tick(30)

        return True
