#game of pong
#first time I'm using git hub
from livewires import games, color
import random

games.init(screen_width = 850, screen_height = 550, fps=45)

class Thing(games.Sprite):
    """parent class for ball and paddles"""
    if self.top>games.screen.height:
        self.top=games.screen.height
    if self.bottom<0:
        self.bottom=0       

class Player(Thing):
    """paddle for player 1"""
    image = games.load_image("player1.png")


def Game(object):
    """the game"""

    def play(self):
        """play the game"""
        #background music
        games.music.load("theme_music.mid")
        games.music.play(-1)

        #set background image
        background_image=games.load_image("background.png")
        games.screen.background = background_image

        #begin
        games.screen.mainloop()

def main():
    pong = Game()
    pong.play()

#run the game
main()
