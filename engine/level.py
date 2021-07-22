from engine import pg, Surface, SpriteSheet, Rect
import os

from player import Knight
from enemy import Beeto

path = os.path.dirname(__file__)
path = os.path.join(path, '../assets/images/plains.png')

sprites = SpriteSheet(path, {
    'bg': (0, 20, 150, 90),
    'g0': (144, 224, 16, 16),
    'g1': (160, 224, 16, 16),
    'g2': (192, 224, 16, 16),
    'g3': (96, 224, 16, 16),
    'g4': (304, 240, 16, 16),
    'g5': (368, 240, 16, 16),
    'g6': (352, 176, 16, 16),
    'ld': (80, 224, 16, 16),
    'sp': (352, 240, 16, 16),
})

sprite_mapping = {
    '[': sprites.sprite('g0'),
    '=': sprites.sprite('g1'),
    ']': sprites.sprite('g2'),
    '|': sprites.sprite('g3'),
    '.': sprites.sprite('g6'),
    'M': sprites.sprite('sp'),
    'H': sprites.sprite('ld'),
}


class Tile:
    def __init__(self, rect, type):
        self.rect = rect
        self.type = type


class Level:
    def __init__(self, data):
        self.tiles = []
        self.entities = []

        with open(data) as file:
            self.array = file.read().split('\n')
            self.w = len(self.array[0])
            self.h = len(self.array)
        self.map = Surface((self.w*16, self.h*16), pg.SRCALPHA)

        self.build_map()

    def build_map(self):
        for i in range(self.h):
            for j in range(self.w):
                k = self.array[i][j]

                if k != ' ':
                    if k not in ('P', 'B'):
                        self.map.blit(sprite_mapping[k], (j*16, i*16))

                        if k == 'H':
                            _type = 'ladder'
                        elif k == 'M':
                            _type = 'spike'
                        else:
                            _type = 'block'

                        self.tiles.append(
                            Tile(Rect(j*16, i*16, 16, 16), _type))
                    elif k == 'P':
                        self.entities.append(
                            Knight(Rect(j*16, i*16-15, 34, 31)))
                    elif k == 'B':
                        self.entities.append(
                            Beeto(Rect(j*16, i*16+1, 26, 15)))
