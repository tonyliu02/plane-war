import pygame
from random import *


class BombSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        self.image = pygame.image.load("images/bomb_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), -100
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), -100
        self.active = True


class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        self.image = pygame.image.load("images/bullet_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), -100
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), -100
        self.active = True
