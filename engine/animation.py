FPS = 60


class Animation:
    def __init__(self, frames, duration, repeat=False, flip_offset=(0, 0)):
        self.i = 0  # animation frame index
        self.j = 0  # game frame index
        self.nframes = len(frames)  # number of animation frames
        # update animation frame every k frames
        self.k = int(FPS / self.nframes * duration)

        self.stopped = False
        self.flip_offset = flip_offset

        self.frames = frames  # animation frames
        self.repeat = repeat  # repeat animation

    def tick(self):
        if not self.stopped:
            if self.j == 0:
                self.i += 1

            self.j += 1

            if not self.repeat and self.i == self.nframes:
                self.stopped = True

            self.i %= self.nframes
            self.j %= self.k

    def reset(self):
        self.i = 0
        self.j = 0
        self.stopped = False

    def frame(self):
        return self.frames[self.i]
