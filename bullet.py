from ursina import *
import time

class Bullet(Entity):
    def __init__(self, position, direction, shooter, enemies, walls_1, walls_2):
        super().__init__()
        self.model = 'sphere'
        self.color = color.red
        self.scale = (0.3, 0.3, 0.3)
        self.position = Vec3(position.x, position.y + 1.2, position.z)
        self.direction = direction.normalized()
        self.speed = 45
        self.collider = 'sphere'
        self.hit_sound = Audio('assets/sounds/2.mp3', autoplay=False)

        self.shooter = shooter
        self.enemies = enemies
        self.walls_1 = walls_1
        self.walls_2 = walls_2

    def update(self):
        self.position += self.direction * self.speed * time.dt

        hit_info = self.intersects()

        if hit_info.hit:
            if hit_info.entity == self.shooter.player:
                self.shooter.lose_life()
                self.disable()
            elif hit_info.entity in self.enemies:
                hit_info.entity.lose_life()
                self.disable()
                self.hit_sound.play()
            elif hit_info.entity in self.walls_1 or hit_info.entity in self.walls_2:
                self.disable()

        if abs(self.position.x) > 100 or abs(self.position.z) > 100:
            self.disable()