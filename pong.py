#game of pong
#first time I'm using git hub
from livewires import games, color
import random

games.init(screen_width = 850, screen_height = 550, fps=45)


#################
#Base Classes####
#################
class Thing(games.Sprite):
    """parent class for ball and paddles"""
    def update(self):
        if self.top<0:
            self.top=0
        if self.bottom>games.screen.height:
            self.bottom=games.screen.height

    
class Paddle(Thing):
    """player or computer paddle"""
    SPEED=3#how fast paddle moves up and down
    
    def move_up(self):
        self.y -= Paddle.SPEED

    def move_down(self):
        self.y += Paddle.SPEED
        

##############
#Ball#########
##############
class Ball(Thing):
    image = games.load_image("ball.png")
    SPEED = 4#speed multiplier

    bounce_sound  = games.load_sound("bounce.WAV")

    acceleration = 0.15#how quickly ball speed increases

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

        if self.overlapping_sprites:#ball has contacted a paddle

            #play bounce sound
            Ball.bounce_sound.play()

            #increase side-to-side speed
            if self.dx > 0:
                self.dx += Ball.acceleration
            elif self.dx < 0:
                self.dx -= Ball.acceleration
            #change side-to-side direction after contacting a paddle
            self.dx= -self.dx

            #change up/down speed based on where ball hit the paddle
            for paddle in self.overlapping_sprites:
                paddle_y = paddle.y
                #paddle is 75 px high
            ball_y = self.y

            if abs(ball_y - paddle_y) > 10:#ball didnt hit midddle 20 of paddle
                dist = ball_y - paddle_y
                change = dist / 30
                #change dy based on how far ball was from center of paddle
                self.dy += change
            


        
        #end game if ball is off screen
        if self.left > games.screen.width:
            #ball went off on right side
            if players == 1:
                #1 player game, CPU  wins
                self.game.end(0)
            else:
                #player 2 wins
                self.game.end(2)

        elif self.right < 0:
            #ball went off on left side
            self.game.end(1)  #P1 wins        


        #pause the game if not already paused
        if games.keyboard.is_pressed(games.K_p) and self.game.is_paused == False:
            self.game.pause()
            #remember the speed
            self.paused_dx = self.dx
            self.paused_dy = self.dy
            #set speed to 0
            self.dx = 0
            self.dy = 0

        #resume if game is already paused
        if games.keyboard.is_pressed(games.K_r) and self.game.is_paused:
            self.game.resume()
            #start the ball moving again
            self.dx = self.paused_dx
            self.dy = self.paused_dy
            
        
        
###############
#Player########
###############            

class Player(Paddle):
    """paddle for player 1"""

    def __init__(self, game, x, img, up_key, down_key):
        """create the player's paddle"""
        super(Player, self).__init__(image=img, x=x,
                                     y=games.screen.height / 2)
        self.game=game
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        """move the paddle"""

        super(Player, self).update()
        
        if self.game.is_paused==False:
        #game is not paused
            #keyboard control
            if games.keyboard.is_pressed(self.up_key):
                self.move_up()
            if games.keyboard.is_pressed(self.down_key):
                self.move_down()

        
    
#############
#CPU#########
#############                    
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

        if ball_x < games.screen.width / 2 and ball_x > 0 and self.game.is_paused==False:
            #ball is on computer's half and game is not paused
            if ball_y > self.y:
                self.move_down()
            elif ball_y < self.y:
                self.move_up()
    

################
#Button Class###
################                
class Button(games.Sprite):
    """a pressable button"""

    #game, x, y, img1, img2, click function, value given to click function
    def __init__(self, game, x, y,
                 unpressed_img, pressed_img, function, value=None):
        super(Button, self).__init__(image = unpressed_img, x=x, y=y,
                                     is_collideable = False)
        
        self.game = game
        self.unpressed_img = unpressed_img
        self.pressed_img = pressed_img
        #function to run when clicked
        self.function = function

        #value to pass to the function
        self.value = value
        
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

    def click(self):
        if self.value:
            self.function(self.value)
        else:
            self.function()

class ToggleButton(games.Sprite):
    """button with 2 states that change when clicked"""
    #game, x, y, img1, img2, click function 1, function 2, value 1, value 2
    def __init__(self, game, x, y, unpressed_img,
                pressed_img, function1, function2, value1=None, value2=None):
        
        super(ToggleButton, self).__init__(image = unpressed_img, x=x, y=y,
                                             is_collideable = False)
        self.game = game
        self.unpressed_img = unpressed_img
        self.pressed_img = pressed_img
        #functions to run when clicked
        self.function1 = function1
        self.function2 = function2

        #value to pass to the function
        self.value1 = value1
        self.value2 = value2

    def update(self):
        mouse_x = games.mouse.x
        mouse_y = games.mouse.y

        if mouse_x < self.right and mouse_x > self.left and mouse_y < self.bottom and mouse_y > self.top:
            #mouse is hovering over button

            #get single click state
            self.single_click = self.game.left_click.get_single_click()
            if self.single_click:
                #button has been left-clicked
                self.click()

    def click(self):
        if self.image == self.unpressed_img:
            #button is in state 1, set img to state 2
            self.set_2()
                
        elif self.image == self.pressed_img:
            #button is in state 2, set img to state 1
            self.set_1()

    def set_1(self):
        #set button to state 1
        self.image = self.unpressed_img
        #run function coorelating to 1st img
        if self.value1:
            self.function1(self.value1)
        else:
            self.function1()
            
    def set_2(self):
        #change button to state 2
        self.image = self.pressed_img
        #run function coorelating to 2nd img
        if self.value2:
            self.function2(self.value2)
        else:
            self.function2()
                
class MouseClick(games.Sprite):
    """class to allow the reading of a single left click from the mouse"""
    def __init__(self):
        super(MouseClick, self).__init__(image = games.load_image("pixel.png"),
                                         x=1, y=1, is_collideable = False)
        self.click_state = games.mouse.is_pressed(0)

    def update(self):
        self.old_click_state = self.click_state
        self.click_state = games.mouse.is_pressed(0)

    def get_single_click(self):
        if self.click_state and not self.old_click_state:
            return 1
        else:
            return 0
        

####################
#The Pause Screen###
####################            
class PauseScreen (games.Sprite):
    """image to fade out the screen while paused"""
    image = games.load_image("fade.png")
    def __init__ (self):
        super(PauseScreen, self).__init__(image = PauseScreen.image,
                                          top=0, left = 0,
                                          is_collideable = False)
    def remove(self):
        self.destroy()


#################################
#"press space to begin" message##
#################################        
class StartMessage(games.Text):
    def __init__(self, game):
        super(StartMessage, self).__init__(value = "Press Space To Start",
                                           size = 70,
                                           x = games.screen.width / 2,
                                           y = games.screen.height / 2,
                                           color = color.green,
                                           is_collideable = False)
        self.game = game


    def update(self):
        if games.keyboard.is_pressed(games.K_SPACE):
            self.game.begin()

#######################
#The Game##############
#######################        
class Game(object):
    """the game"""

    def __init__(self):
        """initialize game object"""
        #get the number of players
        self.p1_button = Button(game = self, x=0.25 * games.screen.width,
                               y=games.screen.height/2,
                               unpressed_img = games.load_image("1player.png"),
                               pressed_img = games.load_image("1player2.png"),
                               function = self.start, value = 1)
        games.screen.add(self.p1_button)

        self.p2_button = Button(game = self, x=0.75 * games.screen.width,
                                     y=games.screen.height/2,
                                     unpressed_img = games.load_image("2player.png"),
                                     pressed_img = games.load_image("2player2.png"),
                                     function=self.start, value = 2)
        games.screen.add(self.p2_button)

        #add the toggle music button
        self.toggle_music_button = ToggleButton(game=self, x=15, y=20,
                                                unpressed_img = games.load_image("music.png"),
                                                pressed_img = games.load_image("nomusic.png"),
                                                function1 = self.play_music,
                                                function2 = self.stop_music)
        games.screen.add(self.toggle_music_button)

        #add the single click class
        self.left_click = MouseClick()
        games.screen.add(self.left_click)
        
        #background music
        games.music.load("theme_music.mid")
        self.play_music()

        #set background image
        background_image=games.load_image("background.png")
        games.screen.background = background_image

        #game is not paused
        self.is_paused = False

        #begin
        games.screen.mainloop()

    def start(self, num_players):
        global players
        
        if num_players == 1:
            players = 1
        else:
            players = 2
            
        self.p1_button.destroy()
        self.p2_button.destroy()

        self.play()

    def play(self):
        """wait for the player to be ready, then begin"""
        #put in the music toggle button
        self.toggle_music_button = ToggleButton(game=self, x=15, y=20,
                                                unpressed_img = games.load_image("music.png"),
                                                pressed_img = games.load_image("nomusic.png"),
                                                function1 = self.play_music,
                                                function2 = self.stop_music)
        games.screen.add(self.toggle_music_button)
        #add the single click class
        self.left_click = MouseClick()
        games.screen.add(self.left_click)
        
        self.start_text = StartMessage(game = self)
        games.screen.add(self.start_text)


    def begin(self):
        """start the game after the player is ready"""
        #remove the start text
        self.start_text.destroy()
        
        #create the player's paddle
        self.player1 = Player(game = self,x=games.screen.width - 20,
                              img = games.load_image("player1.png"),
                              up_key=games.K_UP,
                              down_key=games.K_DOWN)
        games.screen.add(self.player1)

        if players == 1:#1 player game:
            #create the computer paddle
            self.cpu = Computer(game = self)
            games.screen.add(self.cpu)
            
        elif players == 2:#2 player game
            #create the P2 paddle
            self.player2 = Player(game = self, x=20,
                                  img = games.load_image("player2.png"),
                                  up_key = games.K_w,
                                  down_key = games.K_s)
            games.screen.add(self.player2)
            
        #create the ball
        self.ball = Ball(game=self)
        games.screen.add(self.ball)
        
    def play_music(self):
        games.music.play(-1)
        
    def stop_music(self):
        games.music.stop()
        
    def pause(self):
        self.is_paused = True
        
        #stop the music
        self.toggle_music_button.set_2()

        #add in fadeout screen
        self.pause_screen = PauseScreen()
        games.screen.add(self.pause_screen)


    def resume(self):
        #restart the music
        self.toggle_music_button.set_1()

        #remove fadeout screen
        self.pause_screen.remove()
        self.is_paused = False


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

        self.win_message = games.Text(value = name + " wins!!!",
                                 size = 50,
                                 color = color.orange,
                                 x=games.screen.width /2,
                                 top = 10,
                                 is_collideable=False)
        games.screen.add(self.win_message)

        #remove the ball
        self.ball.destroy()

        #give player restart and quit options
        self.again_button = Button(game = self, x=0.25 * games.screen.width,
                              y=games.screen.height / 2,
                              unpressed_img = games.load_image("again.png"),
                              pressed_img = games.load_image("again2.png"),
                              function = self.replay)
        self.quit_button = Button(game = self, x = 0.75 * games.screen.width,
                             y = games.screen.height / 2,
                             unpressed_img = games.load_image("quit.png"),
                             pressed_img = games.load_image("quit2.png"),
                             function = self.leave)

        games.screen.add(self.again_button)
        games.screen.add(self.quit_button)

    def replay(self):
        """restart the game"""
        games.screen.clear()#remove all sprites from screen
        self.play()
        
    def leave(self):
        """exit the game"""
        games.screen.quit()


def main():
    pong=Game()
    pong.play()

#run the game
main()
