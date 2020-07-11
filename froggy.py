#Game for gtmk game jam:
#Theme: "Out of control"
import arcade
import random
import math
import time
import sys

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Froggy jumper"
VIEW_MARGIN = 40
class Cursor(arcade.Sprite):
    def __init__(self,texture,scale):
        super().__init__(texture,scale)
        self.is_clicked = False
        self.scale = scale
    def update(self):
        if self.is_clicked:
            self.texture = arcade.load_texture("red.png")
            self.is_clicked = not self.is_clicked
        else:
            self.texture = arcade.load_texture("blue.png")



class Game(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_sprite = None
        self.player_list = None
        self.cursor_list = None
        self.cursor = None
        self.coins = 100
        self.coins_bet = 1
        self.current_amount = 3
        self.current_cursor = 0
        self.key_up = False
        self.key_down = False
        self.key_right = False
        self.key_left = False
        self.send_lilypads = False
        self.lilypad_amount = 10
        self.view_bottom = 0
        self.counter = 1
        self.player_list = arcade.SpriteList()
        self.magic = 1
        self.text_list = arcade.SpriteList()
        self.substracted = False
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
    def setup(self):
        """draw n amount of cursors found in self.current_amount
        called every time we reset?"""
        arcade.set_viewport(0,SCREEN_WIDTH,0,SCREEN_HEIGHT)
        self.counter = 2
        self.lilypad_list = arcade.ShapeElementList()
        self.send_lilypads = False
        scale = 1/32
        self.player_list = arcade.SpriteList()
        for i in range(1, self.current_amount+1):
            self.player_sprite = Cursor("blue.png", scale)
            self.player_sprite.center_x = (SCREEN_WIDTH - self.player_sprite.width-100)/self.current_amount * i  
            self.player_sprite.center_y = 100
            self.player_list.append(self.player_sprite)
        self.substracted = False
        
        
    def create_scores(self,numbermagic = [1, 1]):
        self.scores = []
        while len(self.scores) != self.current_amount:
            self.scores.append(random.randrange(int(1* numbermagic[0] *self.magic), int(10 * numbermagic[1] * self.magic)))
            self.scores = list(dict.fromkeys(self.scores))
            if self.compare_to_list(self.scores,self.scores[0]):
                self.scores[0] += random.randrange(int(1* numbermagic[0] *self.magic), int(10 * numbermagic[1] * self.magic))
                self.scores = list(dict.fromkeys(self.scores))
            

    def compare_to_list(self,alist,num):
        out = 0
        for i in alist:
            if i > out:
                out = i
        if num*1.75 <= out:
            return True
        else:
            return False 

    def create_lilypad(self,x, cap):
        if cap >= self.counter:
            lilypad = arcade.create_rectangle_filled(x, self.counter*50+50, 20, 20, arcade.color.GREEN)
            self.lilypad_list.append(lilypad)
    def draw_game(self):
        if not self.send_lilypads:
                    self.text_list.append(self.text)
            
        self.player_list.draw()
        self.text_list.draw()
        player_score = self.scores[0]
        try: 
            self.text_list.remove(self.text)
        except ValueError:
            pass
        if self.send_lilypads:
 
            for index,player in enumerate(self.player_list):
                lily_x = player.center_x
                self.create_lilypad(lily_x,self.scores[index])
            if self.counter != 0:
                self.lilypad_list.draw()
                arcade.set_viewport(0,SCREEN_WIDTH,self.counter*10,SCREEN_HEIGHT+self.counter*10)
                self.counter = (self.counter + 1) % self.lilypad_amount
                time.sleep(1/6)
            else:
                b = self.scores[0]
                self.scores.sort(reverse = True)
                b = len(self.scores) - self.scores.index(b) - 1
                if b == 0:
                    arcade.draw_text(f"sorry you lost your bet of {self.coins_bet}",200, 400, arcade.color.WHITE,20)
                    
                else:
                    arcade.draw_text(f"you won {self.coins_bet*b}, go you!",200, 400, arcade.color.WHITE,20)
                    self.coins += self.coins_bet*b
                    
                    time.sleep(1)

                self.setup()

    def on_draw(self):
        arcade.start_render()
        # Code to draw the screen goesr here
        self.draw_game()


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.key_up = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.key_down = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right = True
        if key == arcade.key.ENTER:
            self.send_lilypads = True
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.key_up = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.key_down = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right = False
    def on_update(self, delta_time):
        """is called every second, plz do notput prints here @placuszek, ty"""
        how_many_points = {"1":[0.9,1.1],"2": [1.1,0.9],"3": [1.2, 0.8]}
        self.text = arcade.draw_text(f'coins bet = {self.coins_bet} \n total coins = {self.coins}',200, 400, arcade.color.WHITE,20)
        if not self.send_lilypads:
            if self.key_up and self.coins_bet < self.coins:
                self.coins_bet += 1 
            elif self.key_down and self.coins_bet > 1:
                self.coins_bet -= 1

            if self.key_right :
                self.current_cursor = (self.current_cursor + 1) % self.current_amount
            elif self.key_left:
                self.current_cursor = (self.current_cursor - 1) % self.current_amount
            self.create_scores(how_many_points[str(self.current_cursor+1)])
        elif not self.substracted and self.send_lilypads:
            
            self.coins = self.coins - self.coins_bet
            self.substracted = not self.substracted
        self.player_list[self.current_cursor].is_clicked = True

        for i in self.player_list:
            i.update()        
        time.sleep(abs(1/6-delta_time))

def main():
    """ Main method """
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
