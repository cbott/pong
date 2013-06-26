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
    SPEED = 4#speed multiplier

    acceleration = 0.5#how quickly ball speed increases

    def __init__(self, game, x=games.screen.width/2, y=games.screen.height/2):
        """create the ball"""
        side_speed=(random.randint(4,6)/10)#will be dx
        down_speed = 1 - side_speed#will be dy
        
        super(Ball, self).__init__(
            image = Ball.image,
            x=x, y=y,
            dx = side_speed * Ball.SPEED,
            dy = down_speed * Ball.SPEED)
        self.game = game

    def update(self):
        super(Ball, self).update()
        if self.top<=0:
            #hit the top, reverse y direction
            self.dy = -self.dy
        if self.bottom>=games.screen.height:
            #hit bottom, reverse y direction
            self.dy = -self.dy

        if self.overlapping_sprites:
            #change side-to-side direction after contacting a paddle
            self.dx= -self.dx

            #increase speed
            self.dx += Ball.acceleration
            self.dy += Ball.acceleration

        if self.right > games.screen.width:
            self.game.end(0)

        elif self.left < 0:
            self.game.end(1)
            
        
        
    

class Paddle(Thing):
    """player or computer paddle"""
    SPEED=3#how fast paddle moves up and down
    
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

        #keyboard control
        if control == "k":
            if games.keyboard.is_pressed(games.K_UP):
                self.move_up()
            if games.keyboard.is_pressed(games.K_DOWN):
                self.move_down()
    


        #mouse control
        else:
            if games.mouse.y > self.y:
                self.move_down()
            elif games.mouse.y < self.y:
                self.move_up()
        
    

class Computer(Paddle):
    """computer player"""
    image = games.load_image("computer.png")

    def __init__ (self, game, x=20):
        """create computer paddle"""
        super(Computer, self).__init__(image = Computer.image,
                                       x=x, y=games.screen.height / 2)
        self.game = game

    def update(self):
        super(Computer, self).update()
        
        ball_y = self.game.ball.y#up and down

        ball_x = self.game.ball.x#side to side

        if ball_x < games.screen.width / 2 and ball_x > 0:#ball is on computer's half
            if ball_y > self.y:
                self.move_down()
            elif ball_y < self.y:
                self.move_up()
    

class Button(games.Sprite):
    """a pressable button"""

    def update(self):
        mouse_x = games.mouse.x
        mouse_y = games.mouse.y

        if mouse_x < self.right and mouse_x > self.left and mouse_y < self.bottom and mouse_y > self.top:
            #mouse is hovering over button
            self.image = self.pressed_img
            if games.mouse.is_pressed(0):
                #button has been left-clicked
                self.click()
        else:
            self.image = self.unpressed_img

class K_Board_Button(Button):
    """button clicked to use keyboard controls"""
    unpressed_img = games.load_image("k_bttn_unpressed.png")
    pressed_img = games.load_image("k_bttn_pressed.png")
        
    def __init__(self, game, x=0.25 * games.screen.width, y=games.screen.height/2):
        super(K_Board_Button, self).__init__(image = K_Board_Button.unpressed_img,
                                             x=x, y=y)
        self.game = game

    def update(self):
        super(K_Board_Button, self).update()

    def click(self):
        self.game.start("kb")

class Mouse_Button(Button):
    """button clicked to use mouse controls"""
    unpressed_img = games.load_image("m_bttn_unpressed.png")
    pressed_img = games.load_image("m_bttn_pressed.png")
        
    def __init__(self, game, x=0.75 * games.screen.width, y=games.screen.height/2):
        super(Mouse_Button, self).__init__(image = Mouse_Button.unpressed_img,
                                             x=x, y=y)
        self.game = game

    def update(self):
        super(Mouse_Button, self).update()

    def click(self):
        self.game.start("m")    


class Game(object):
    """the game"""

    def __init__(self):
        """initialize game object"""
        #get control type
        self.k_button = K_Board_Button(game = self)
        games.screen.add(self.k_button)

        self.m_button = Mouse_Button(game = self)
        games.screen.add(self.m_button)

        games.screen.mainloop()

    def start(self, control_type):
        global control
        
        if control_type == "kb":
            control = "k"
        else:
            control = "m"
            
        self.k_button.destroy()
        self.m_button.destroy()

        self.play()

    def play(self):
        """play the game"""
        #create the player's paddle
        self.player1 = Player(game = self,x=games.screen.width - 20)
        games.screen.add(self.player1)

        #create the computer paddle
        self.cpu = Computer(game = self)
        games.screen.add(self.cpu)

        #create the ball
        self.ball = Ball(game=self)
        games.screen.add(self.ball)

        
        #background music
        games.music.load("theme_music.mid")
        games.music.play(-1)

        #set background image
        background_image=games.load_image("background.png")
        games.screen.background = background_image

        #begin
        games.screen.event_grab = False
        


    def end(self, winner):
        #0=computer
        #1=player 1
        #2=player 2
        if winner == 0:
            name = "Computer"
        elif winner == 1:
            name = "Player 1"
        elif winner == 2:
            name = "Player 2"

        win_message = games.Text(value = name + " wins!!!",
                                 size = 50,
                                 color = color.orange,
                                 x=games.screen.width /2,
                                 y = games.screen.height /2,
                                 is_collideable=False)
        games.screen.add(win_message)
        
        

def main():
    pong=Game()
    pong.play()

#run the game
main()
