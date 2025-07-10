from ursina import *

class HUDManager:
    def __init__(self):
        self.lives_text = Text(text='', position=(-0.45, 0.45), scale=2, color=color.white)
        self.level_text = Text(text='', position=(-0.45, 0.4), scale=2, color=color.white)
        self.game_over_text = None
        self.win_text = None
        self.buttons = []

    def update_lives(self, lives):
        self.lives_text.text = f'Lives: {lives}'

    def update_level(self, level):
        self.level_text.text = f'Level: {level}'

    def show_game_over(self, on_restart, on_exit):
        if not self.game_over_text:
            self.game_over_text = Text('Game Over', position=(0, 0.2), scale=2, color=color.red)

        self.buttons = [
            Button(text='Restart', position=(0, -0.2), scale=(0.2, 0.05), color=color.green, on_click=on_restart),
            Button(text='Exit', position=(0, -0.3), scale=(0.2, 0.05), color=color.red, on_click=on_exit)
        ]

        mouse.visible = True

    def show_victory(self, on_restart, on_exit):
        if not self.win_text:
            self.win_text = Text('You Win!', position=(0, 0.2), scale=2, color=color.green)

        self.buttons = [
            Button(text='Restart', position=(0, -0.2), scale=(0.2, 0.05), color=color.green, on_click=on_restart),
            Button(text='Exit', position=(0, -0.3), scale=(0.2, 0.05), color=color.red, on_click=on_exit)
        ]

        mouse.visible = True

    def clear_messages_and_buttons(self):
        if self.game_over_text:
            self.game_over_text.disable()
            self.game_over_text = None
        if self.win_text:
            self.win_text.disable()
            self.win_text = None
        for btn in self.buttons:
            btn.disable()
        self.buttons.clear()
        mouse.visible = False