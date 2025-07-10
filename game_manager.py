from ursina import *
from scene import SceneBuilder
from hud import HUDManager
from shooter import Shooter
from enemy import Enemy

class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.hud = HUDManager()
        self._create_everything()

    def _create_everything(self):
        self.scene_builder = SceneBuilder()
        self.ground, self.walls_1, self.walls_2, self.borders = self.scene_builder.build()

        self.enemies = []
        self.shooter = Shooter(self.enemies, self.walls_1, self.walls_2, self.hud,
                               on_restart=self.restart,
                               on_exit=self.exit)

        for _ in range(3):
            pos = Vec3(random.uniform(0, 50), 0, random.uniform(-50, 50))
            enemy = Enemy(pos, self.shooter, self.walls_1, self.walls_2, self.enemies)
            self.enemies.append(enemy)

    def restart(self):
        for e in self.enemies:
            destroy(e)
        self.enemies.clear()

        if self.shooter:
            self.shooter.background_music.stop()
            destroy(self.shooter)

        if self.scene_builder.ground:
            destroy(self.scene_builder.ground)
        for w in self.scene_builder.walls_1 + self.scene_builder.walls_2 + self.scene_builder.borders:
            destroy(w)

        self.hud.clear_messages_and_buttons()
        self._create_everything()

    def exit(self):
        application.quit()

    def input(self, key):
        if key == 'escape':
            self.exit()