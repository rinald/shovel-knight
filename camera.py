from engine import *


class Camera:
    def __init__(self, pos=[0, 0]):
        self.pos = pos
        self.vx = 0

    def move(self, player):
        self.pos[0] += self.vx*dt

        if player.rect.x > 200-16 and player.rect.x < 600-16:
            if player.collision['left'] or player.collision['right']:
                self.vx = 0
            else:
                self.vx = player.vx

        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vx = 0
        elif self.pos[0] > 400:
            self.pos[0] = 400
            self.vx = 0
