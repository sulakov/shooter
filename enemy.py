from ursina import *
import random
import math
import time
from bullet import Bullet

class Enemy(Entity):
    def __init__(self, position, shooter, walls_1, walls_2, enemies):
        super().__init__()
        self.model = 'assets/models/sin_nombre1.glb'
        self.texture = 'assets/textures/с.jpeg'
        self.scale = (0.3, 0.3, 0.3)
        self.position = position
        self.shooter = shooter
        self.walls_1 = walls_1
        self.walls_2 = walls_2
        self.enemies = enemies
        self.shoot_delay = random.uniform(5, 10)
        self.last_shot = time.time() + random.uniform(0, 2)
        self.speed = 0.9
        self.collider = 'box'
        self.health = 3
        self.direction = self.generate_random_direction()
        self.next_direction_change = time.time() + 5

    def generate_random_direction(self):
        while True:
            direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1))
            if direction.length() > 0.1:
                return direction.normalized()

    def update(self):
        if time.time() >= self.next_direction_change:
            self.direction = self.generate_random_direction()
            self.next_direction_change = time.time() + 5

        self.position += self.direction * self.speed * time.dt

        if abs(self.position.x) > 50:
            self.position.x = 50 * math.copysign(1, self.position.x)
        if abs(self.position.z) > 50:
            self.position.z = 50 * math.copysign(1, self.position.z)

        if time.time() - self.last_shot >= self.shoot_delay:
            self.shoot()
            self.last_shot = time.time()

    def shoot(self):
        direction = (self.shooter.player.position - self.position).normalized()
        start_pos = self.position + direction * 2
        Bullet(start_pos, direction, self.shooter, self.enemies, self.walls_1, self.walls_2)

    def lose_life(self):
        self.health -= 1
        if self.health <= 0:
            self.disable()
            
# placeholder for further development
class Boss(Enemy):
    def __init__(self, position, shooter, walls_1, walls_2, enemies):
        super().__init__(position, shooter, walls_1, walls_2, enemies)
        self.scale = (0.5, 0.5, 0.5)
        self.shoot_delay = random.uniform(2, 5)
        self.speed = 1.2