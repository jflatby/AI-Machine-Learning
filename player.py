import pygame
from vec2d import Vec2d
import numpy as np


class Player(pygame.sprite.Sprite):

    def __init__(self, food):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("sprites/player.png").convert()
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.food = food
        self.points = 0
        self.got_point = False
        self.dead = False

        self.max_speed = 15
        self.turn_speed = 10
        self.turning = 0

        self.direction = Vec2d(0, 1)
        self.acceleration = Vec2d(0, 0)
        self.velocity = Vec2d(0, 0)
        self.position = Vec2d(400, 500)#Vec2d(self.rect.x, self.rect.y)
        self.rect.center = (self.position.x, self.position.y)

    def turn_right(self):
        self.turning = -1

    def turn_left(self):
        self.turning = 1

    def stop_turning(self):
        self.turning = 0

    def turn(self, dir):#-1 = left, 1 = right

        #Rotate direction vector
        self.direction.rotate(dir * self.turn_speed)

        #Rotate original image and set as new image
        self.image = pygame.transform.rotate(self.original_image, self.direction.get_angle() - 90)

        #Remember center coords
        x, y = self.rect.center

        #Assign new rect and position at the old center coordinates
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position = Vec2d(x, y)


    def move(self):
        """
        Called every frame
        """

        if(self.turning != 0):
            self.turn(self.turning)

        self.velocity = self.direction * self.max_speed

        ##update position
        self.position.x += self.velocity.x
        self.position.y -= self.velocity.y

        self.rect.center = (self.position.x, self.position.y)

    def die(self):
        self.dead = True

    def perform_actions(self, output):
        if output[0]:
            self.turn_left()
        if output[1]:
            self.turn_right()

        if not output[0] and not output[1]:
            self.stop_turning()

    def reset(self):
        self.position = Vec2d(400, 500)
        self.direction = Vec2d(0, 1)
        self.velocity = Vec2d(0, 0)
        self.acceleration = Vec2d(0, 0)
        self.rect.center = (self.position.x, self.position.y)
        self.points = 0
