from abc import ABC, abstractmethod
from . import *


class Entity(ABC):
    def __init__(self, rect=Rect(0, 0, 0, 0), sprites=None, animations={}):
        self.rect = rect
        self.flip = False
        self.sprite = None
        self.sprites = sprites
        self.animation = None
        self.animations = animations
        self.collision = {'left': False, 'right': False,
                          'top': False, 'bottom': False}
        self.vx = 0
        self.vy = 0

    def draw(self, surface, offset=(0, 0)):
        pos = [self.rect.x-offset[0], self.rect.y-offset[1]]

        if self.flip == True and self.animation is not None:
            if self.animation.i != 0:
                pos[0] -= self.animation.flip_offset[0]

        surface.blit(self.sprite, pos)

    def set_sprite(self, sprite_id=None):
        if sprite_id is None:
            sprite = self.animation.frame()
        else:
            sprite = self.sprites.sprite(sprite_id)

        if self.flip:
            sprite = pg_transform.flip(sprite, 1, 0)

        self.sprite = sprite

    def collisions(self, tiles):
        hit_list = []

        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def animate(self):
        if self.animation is not None:
            self.animation.tick()
            self.set_sprite()

            if self.animation.stopped == True:
                self.animation = None
                self.set_sprite('idle')

    def set_animation(self, animation_id):
        self.animation = self.animations[animation_id]
        self.animation.reset()

    def update(self, tiles):
        self.move(tiles)
        self.animate()

    @abstractmethod
    def on_event(self, event):
        ...

    @abstractmethod
    def move(self, tiles):
        ...
