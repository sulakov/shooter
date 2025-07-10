import os
from ursina import *
from game_manager import GameManager

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

app = Ursina()

manager = GameManager()

window.fullscreen = True

app.run()