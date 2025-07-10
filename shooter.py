from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
import random
from bullet import Bullet
from enemy import Enemy
from hud import HUDManager

class Shooter(Entity):
    def __init__(self, enemies, walls_1, walls_2, hud: HUDManager, on_restart=None, on_exit=None):
        super().__init__()
        self.enemies = enemies
        self.walls_1 = walls_1
        self.walls_2 = walls_2
        self.hud = hud
        self.on_restart = on_restart
        self.on_exit = on_exit

        self.player = FirstPersonController()
        self.player.collider = 'capsule'
        self.shoot_delay = 0.5
        self.last_shot = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.win = False

        self.player.position = Vec3(-25, 0, 0)

        self.visible_model = Entity(
            parent=self.player.camera_pivot,
            model='assets/models/Sunstreaker_Weapon__ARM.glb',
            texture='assets/models/wep_shankfeathering_1.png',
            position=(0.3, -0.5, 1),
            scale=(0.2, 0.2, 0.3),
            rotation=(0, 90, 0),
            color=color.black10
        )

        if hasattr(self, 'background_music'):
            self.background_music.stop()
            destroy(self.background_music)

        self.shoot_sound = Audio('assets/sounds/warfare-laser-blast_fjdw5t4u.mp3', autoplay=False)
        self.background_music = Audio('assets/sounds/background_music.mp3', loop=True)
        self.background_music.play()

        self.hud.update_lives(self.lives)
        self.hud.update_level(self.level)

    def update(self):
        if self.game_over or self.win:
            return
        if held_keys['left mouse'] and time.time() - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = time.time()
        self.check_level_complete()

    def shoot(self):
        position = self.player.position
        direction = self.player.forward
        Bullet(position + direction, direction, self, self.enemies, self.walls_1, self.walls_2)
        self.shoot_sound.play()

    def lose_life(self):
        self.lives -= 1
        self.hud.update_lives(self.lives)
        if self.lives <= 0:
            self.game_over = True
            self.hud.show_game_over(self.on_restart, self.on_exit)
            self.player.disable()

    def check_level_complete(self):
        if all(not enemy.enabled for enemy in self.enemies):
            self.level += 1
            if self.level > 5:
                self.win = True
                self.hud.show_victory(self.on_restart, self.on_exit)
                self.player.disable()
            else:
                self.spawn_next_level()

    def spawn_next_level(self):
        self.lives = 3
        self.hud.update_lives(self.lives)
        self.hud.update_level(self.level)

        enemies_count = {
            1: 3,
            2: 4,
            3: 5,
            4: 6,
            5: 7
        }.get(self.level, 3)

        self.enemies.clear()

        for _ in range(enemies_count):
            x = random.uniform(0, 50)
            z = random.uniform(-50, 50)
            pos = Vec3(x, 0, z)
            enemy = Enemy(pos, self, self.walls_1, self.walls_2, self.enemies)
            self.enemies.append(enemy)