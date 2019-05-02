import pygame
from vec2d import Vec2d
import random

class Food(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/food.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.position = Vec2d(200, 150)
        self.rect.center = (self.position.x, self.position.y)

    def respawn(self):
        self.position = Vec2d(random.randint(100, 700), random.randint(100, 500))
        self.rect.center = (self.position.x, self.position.y)