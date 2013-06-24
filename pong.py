#game of pong
#first time I'm using git hub
from livewires import games, color
import random

games.init(screen_width = 850, screen_height = 550, fps=45)

class Thing(games.Sprite):
    """parent class for ball and paddles"""
    def update(self):
        if self.top<0:
            self.top=0
        if self.bottom>games.screen.height:
            self.bottom=games.screen.height       

class Ball(Thing):
    image = games.load_image("ball.png")
    SPEED = 3#speed multiplier

    def __init__(self, x=games.screen.width/2, y=games.screen.height/2):
        """create the ball"""
        super(Ball, self).__init__(
            image = Ball.image,
            x=x, y=y,
            dx = random.random() * Ball.SPEED,
            dy=random.random() * Ball.SPEED)

    def update(self):
        super(Ball, self).update()
        if self.top<=0:
            #hit the top, reverse y direction
            self.dy = -self.dy
        if self.bottom>=games.screen.height:
            #hit bottom, reverse y direction
            self.dy = -self.dy
        
        
    

class Paddle(Thing):
    """player or computer paddle"""
    SPEED=2#how fast paddle moves up and down
    
    def move_up(self):
        self.y -= Paddle.SPEED

    def move_down(self):
        self.y += Paddle.SPEED
        
        

class Player(Paddle):
    """paddle for player 1"""
    image = games.load_image("player1.png")

    def __init__(self, game, x):
        """create the player's paddle"""
        super(Player, self).__init__(image=Player.image, x=x,
                                     y=games.screen.height / 2)
        self.game=game

    def update(self):
        """moove the paddle"""

        super(Player, self).update()

        if games.keyboard.is_pressed(games.K_UP):
            self.move_up()
        if games.keyboard.is_pressed(games.K_DOWN):
            self.move_down()
    

    
    


class Game(object):
    """the game"""

    def __init__(self):
        """initialize game object"""
        #create the player's paddle
        self.player1 = Player(game = self,x=games.screen.width - 20)
        games.screen.add(self.player1)

        #create the ball
        self.ball = Ball()
        games.screen.add(self.ball)

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
    pong=Game()
    pong.play()

#run the game
main()
