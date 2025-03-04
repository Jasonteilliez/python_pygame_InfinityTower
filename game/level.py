import pygame
from settings import *
from tile import Tile
from player import Player
from map import Map
from support import import_folder

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        map = Map()

        layouts = {
            'boundary': map.boundary,
            'levels': map.floor,
            'entities': map.entities
        }

        graphics = {
            'levels' : import_folder('graphics/level')
        }
        
        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == "levels":
                            surf = graphics['levels'][int(col)]
                            Tile((x,y), [self.visible_sprites], 'levels', surf)

                        if style == 'entities':
                            if col == 'P':
                                self.player = Player((x,y),[self.visible_sprites], 'player', self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/test/background100x100.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (-700,-700))

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset*0.7
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in self.sprites():
        # for sprite in sorted(self.sprites(), key = lambda sprite : sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)