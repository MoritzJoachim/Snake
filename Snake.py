import random
import time
from enum import Enum

# Snake game
# 10x10 RGB LED Matrix "Snake" game
# LED strip configuration:
LED_COUNT = 100  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA = 5  # DMA channel to use for generating signal
LED_BRIGHTNESS = 155  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

# setting up the class for the direction variable, this variable is used to change the outcome of 'right' or 'left' button input
class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    # making sure that after adding 1 to 3 the outcome isn't 4 but 0 - resulting in the list starting from the beginning again
    def succ(self):
        if self is Direction.UP:
            return Direction.RIGHT
        else:
            return Direction(self.value + 1)

    # doing the same here but for the other direction
    def pred(self):
        if self is Direction.RIGHT:
            return Direction.UP
        else:
            return Direction(self.value - 1)

# setting up the class for button input
class ButtonPress(Enum):
    LEFT = 0
    RIGHT = 1

# setup of the main snake class
class Snake:
    # setting up the initial variables
    def __init__(self):
        # setting the starting position
        self.current_locations = [42]
        # getting the first random fruit drop (that is not occupied by the snake)
        self.fruit_location = random.choice([x for x in list(range(1, 100)) if x not in self.current_locations]) 
        # printing for testing purposes in console
        print("the fruit location is: " + str(self.fruit_location))
        # setting the starting direction (from left to right)
        self.direction = Direction.RIGHT    
        self.alive = True
        self.set_random_fruit_drop()

    def is_alive(self):
        return self.alive

    # defining the function for the button input with our enumerated values from (class ButtonPress(Enum))
    def button_input(self, button_pressed):
        # making sure the direction change upon button press is correct (-1 in the Direction class for LEFT and +1 for RIGHT)
        if button_pressed is ButtonPress.LEFT:
            self.direction = self.direction.pred()
        elif button_pressed is ButtonPress.RIGHT:
            self.direction = self.direction.succ()

    # setting up the function that generates a random available space for the fruit drop
    def set_random_fruit_drop(self):
        # this is done by generating a value between 1 and 100 and comparing it with the current snake locations
        self.fruit_location = random.choice([x for x in list(range(1, 100)) if x not in self.current_locations])
        print("the fruit location is: " + str(self.fruit_location))

    # setting up the function that checks if the snake runs into itself
    def check_collision_self(self, location_to_move_to):
        # this is done by comparing the pixel the snake is about to go to with all the current snake positions except for the head itself
        if location_to_move_to in self.current_locations[1:]:
            return True
        else:
            return False

    # setting up the function that checks if the snake collects a piece of fruit
    def check_collision_fruit(self, location_to_move):
        # this is done by comparing the pixel the snake is about to go to with the current fruit location
        if location_to_move is self.fruit_location:
            return True
        else:
            return False

    # setting up the main looped function that runs while the snake is alive (general movement of the snake including all the collision checks)
    def move(self):
        # printing is only for testing purposes
        print("current location is:" + self.current_locations.__str__())
        # the head position of the snake is the last entry in the 'current_locations' array
        head_pos = self.current_locations[-1]

        # setting up the general movements depending on location and direction. Button input is irrelevant since we change the direction directly after input - this makes us only able to go "straight"
        if self.direction is Direction.RIGHT:
            # if the direction is right and the head of the snake is at the right edge of the matrix, it moves out and reenters on the ledt edge (no penalty for going over the borders in this game)
            if head_pos % 10 == 0:
                move_location = head_pos - 9
            else:
                # otherwise just moving  one pixel to the right
                move_location = head_pos + 1

        elif self.direction is Direction.DOWN:
            # if the direction is down and the head of the snake is at the bottom edge of the matrix, it moves out and reenters on the top side
            if head_pos >= 91:
                move_location = head_pos - 90
            else:
                # otherwise just moving one pixel down
                move_location = head_pos + 10

        elif self.direction is Direction.LEFT:
            # if the direction is left and the head of the snake is at the left edge of the matrix, it moves out and reenters on the right side
            if head_pos % 10 == 1:
                move_location = head_pos + 9
            else:
                # otherwise just moving one pixel to the left
                move_location = head_pos - 1

        elif self.direction is Direction.UP:
            # if the direction is up and the head of the snake is at the top edge of the matrix, it moves out and reenters on the bottom side
            if head_pos <= 10:
                move_location = head_pos + 90
            else:
                # otherwise just moving one pixel up
                move_location = head_pos - 10
        # now we have stored the position the snake is about to move in the variable "move_location", it hasn't actually moved yet. This way we can check for self collision before the snake actually moves
        # checking for collision with the rest of the snakes body, if the previously defined function returns True, it's game over, or 'self.alive = False'
        if self.check_collision_self(move_location) is True:
            self.alive = False
            return

        # appending the location the head of the snake is about to move to to the array of all locations
        self.current_locations.append(move_location)
        
        # checking if fruit was consumed
        if self.check_collision_fruit(move_location) is True:
            # if fruit was consumed the tail end stays the same and a new random fruit drop is created. (Tail stays the same because a moving head and stationary tail result in a 1 pixel longer snake)
            self.set_random_fruit_drop()
        else:
            # removes the first entry of the array, the tail. (Since the head already moved and no fruit was consumed, getting rid of the tail resulting in a moving snake that stays the same length)
            self.current_locations.pop(0)
        # printing information for testing
        print("current positions are" + self.current_locations.__str__())
        

# this is the main loop, while the snake is alive it checks for button input and just loops snake.move()
snake = Snake()
print(snake.is_alive())
while snake.is_alive() is False:
    print("Game Over")

while snake.is_alive() is True:
    # this delay is used as the speed of the snake
    time.sleep(0.5)
    # this keyboard input will later be replaced by actual button input, this is still run in console
    keyboard_input = input()
    if keyboard_input is "r":
        snake.button_input(ButtonPress.RIGHT)
    elif keyboard_input is "l":
        snake.button_input(ButtonPress.LEFT)
    snake.move()