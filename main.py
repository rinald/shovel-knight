from config import *
from engine import *

from engine.level import sprites

from camera import Camera

HALF_WINDOW_SIZE = (i//2 for i in WINDOW_SIZE)


class ShovelKnight(Game):
    def init(self):
        self.level = Level('assets/levels/level_1.txt')

        self.add_listener(0)

        self.camera = Camera()

        pg_mixer.music.set_volume(0.0)
        pg_mixer.music.load('assets/sounds/music.ogg')
        pg_mixer.music.play(loops=-1)

    def draw(self):
        self.surface.blit(sprites.sprite(
            'bg', size=HALF_WINDOW_SIZE), (0, 0))

        view = self.level.map.subsurface(
            tuple(self.camera.pos) + HALF_WINDOW_SIZE)

        self.surface.blit(view, (0, 0))

        for entity in self.level.entities:
            entity.draw(self.surface, offset=(self.camera.pos[0], 0))

        self.screen.blit(pg_transform.scale(self.surface, WINDOW_SIZE), (0, 0))

    def update(self):
        for entity in self.level.entities:
            entity.update(self.level.tiles)

        self.camera.move(self.level.entities[0])


game = ShovelKnight(TITLE, WINDOW_SIZE, fps=FPS)
game.run()
