from engine import *
from engine.entity import Entity

from config import FPS

sprites = SpriteSheet('assets/images/knight.png', {
    'idle': (2, 2, 34, 32),
    'down_thrust': (2, 223, 24, 36),
    'walk': [(2+42*i, 77, 40, 35) for i in range(5)],
    'jump': (2, 114, 31, 34),
    'fall': (2, 150, 33, 34),
    'slash': [(2+56*i, 186, 54, 35) for i in range(5)],
    # 'shine': [(2+36*i, 323, 34, 32) for i in range(3)],
})

animations = {
    'walk': Animation(sprites.animation_sprites('walk'), duration=0.5, repeat=True),
    'slash': Animation(sprites.animation_sprites('slash'), duration=0.5, repeat=False, flip_offset=(20, 0)),
}


class Knight(Entity):
    def __init__(self, rect=Rect(0, 0, 0, 0)):
        super().__init__(rect, sprites=sprites, animations=animations)

        self.grounded = True
        self.falling = False
        self.down_attack = False

        self.set_sprite('idle')

        self.slash_sound = pg_mixer.Sound('assets/sounds/knight_slash.ogg')
        self.jump_sound = pg_mixer.Sound('assets/sounds/knight_jump.ogg')
        self.land_sound = pg_mixer.Sound('assets/sounds/knight_land.ogg')

    def on_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.flip = True
                self.vx = -10
                if self.grounded:
                    self.set_animation('walk')
            if event.key == K_RIGHT:
                self.flip = False
                self.vx = 10
                if self.grounded:
                    self.set_animation('walk')
            if event.key == K_UP:
                if self.grounded:
                    self.jump_sound.play()
                    self.vy = -40
                    self.grounded = False
                    self.animation = None
                    self.set_sprite('jump')
            if event.key == K_DOWN:
                if not self.grounded:
                    self.down_attack = True
                    self.set_sprite('down_thrust')
            if event.key == K_SPACE:
                self.slash_sound.play()
                self.set_animation('slash')
        if event.type == KEYUP:
            if event.key in (K_LEFT, K_RIGHT):
                self.animation = None
                self.vx = 0
                if self.grounded:
                    self.set_sprite('idle')

    def move(self, tiles):
        self.collision = {'left': False, 'right': False,
                          'top': False, 'bottom': False}

        if self.vx != 0:
            self.rect.x += self.vx*dt
            hit_list = self.collisions(tiles)

            for tile in hit_list:
                if self.vx > 0:
                    if tile.type != 'ladder':
                        self.rect.right = tile.rect.left
                        self.collision['right'] = True
                elif self.vx < 0:
                    if tile.type != 'ladder':
                        self.rect.left = tile.rect.right
                        self.collision['left'] = True

        self.rect.y += self.vy*dt
        self.vy += 0.5*g*dt**2

        if self.vy > 9:
            if self.grounded:
                self.grounded = False
                self.animation = None
                self.set_sprite('fall')

        hit_list = self.collisions(tiles)

        for tile in hit_list:
            if self.vy > 0:
                if tile.type != 'ladder':
                    self.rect.bottom = tile.rect.top
                    self.collision['bottom'] = True
            elif self.vy < 0:
                if tile.type != 'ladder':
                    self.rect.top = tile.rect.bottom
                    self.collision['top'] = True

        if not self.falling and self.vy > 0 and not self.grounded:
            if not self.down_attack:
                self.set_sprite('fall')
            self.falling = True

        if self.collision['bottom'] == True:
            self.vy = 0

            if not self.grounded:
                self.land_sound.play()

                if self.vx != 0:
                    self.set_animation('walk')
                else:
                    self.set_sprite('idle')

            self.grounded = True
            self.falling = False
            self.down_attack = False

        if self.collision['top'] == True:
            self.vy = 0
