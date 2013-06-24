#game of pong
#first time i'm using git hub
from livewires import games, color
import random

games.init(screen_width = 850, screen_height = 550, fps=45)

class Thing(games.Sprite):
    """parent class for ball and paddles"""
    if self.top>games.screen.height:
        self.top=games.screen.height
    if self.bottom<0:
        self.bottom=0       
