import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = pygame.image.load('graphics/player/down/1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-32,-32)

        self.direction = pygame.math.Vector2()
        self.speed = 10

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_o]:
            self.direction.y = -1
        elif keys[pygame.K_l]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_k]:
            self.direction.x = -1
        elif keys[pygame.K_m]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0 :
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0 :
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0 :
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0 :
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)
        