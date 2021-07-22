from abc import ABC, abstractmethod
import sys

from . import *


class Game(ABC):
    def __init__(self, title, window_size, fps=60):
        self.title = title
        self.window_size = window_size
        self.fps = fps

        pg_mixer.pre_init(44100, -16, 1, 512)
        pg_mixer.init()
        pg.init()

        pg_display.set_caption(title)

        self.screen = pg_display.set_mode(window_size)
        self.surface = Surface(tuple((i/2 for i in window_size)))
        self.clock = pg_time.Clock()
        self.entity_pool = []
        self.event_listeners = []

    def add_listener(self, i):
        self.event_listeners.append(i)

    def run(self):
        self.init()

        while True:
            for event in pg_event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

                for i in self.event_listeners:
                    self.level.entities[i].on_event(event)

            self.draw()
            self.update()

            pg_display.update()
            self.clock.tick(self.fps)

    @abstractmethod
    def init(self):
        ...

    @abstractmethod
    def draw(self):
        ...

    @abstractmethod
    def update(self):
        ...
