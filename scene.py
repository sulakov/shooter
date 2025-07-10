from ursina import *
import random

class SceneBuilder:
    def __init__(self):
        self.walls_1 = []
        self.walls_2 = []
        self.borders = []
        self.ground = None

    def build(self):
        self._build_ground()
        self._build_walls()
        self._build_borders()
        Sky()
        return self.ground, self.walls_1, self.walls_2, self.borders

    def _build_ground(self):
        self.ground = Entity(model='plane', texture='grass', collider='mesh', scale=(100, 1, 100))

    def _build_walls(self):
        self.walls_1 = [
            Entity(model='cube', texture='brick', position=(random.uniform(-50, 50), 0, random.uniform(-50, 50)),
                   scale=(2, 5, 1), collider='box') for _ in range(23)
        ]
        self.walls_2 = [
            Entity(model='cube', texture='brick', position=(random.uniform(-50, 50), 0, random.uniform(-50, 50)),
                   scale=(1, 5, 2), collider='box') for _ in range(26)
        ]

    def _build_borders(self):
        t = 1
        self.borders = [
            Entity(position=(-50, 0, 0), scale=(t, 5, 100), collider='box', model=None),
            Entity(position=(50, 0, 0), scale=(t, 5, 100), collider='box', model=None),
            Entity(position=(0, 0, 50), scale=(100, 5, t), collider='box', model=None),
            Entity(position=(0, 0, -50), scale=(100, 5, t), collider='box', model=None),
        ]