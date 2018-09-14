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
# LED strip configuration\


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def succ(self):
        if self is Direction.UP:
            return Direction.RIGHT
        else:
            return Direction(self.value + 1)

    def pred(self):
        if self is Direction.RIGHT:
            return Direction.UP
        else:
            return Direction(self.value - 1)


class ButtonPress(Enum):
    LEFT = 0
    RIGHT = 1


class Snake:
    def __init__(self):
        self.current_locations = [42]
        self.fruit_location = random.choice([x for x in list(range(1, 100)) if x not in self.current_locations]) 
        print("the fruit location is: " + str(self.fruit_location))
        self.direction = Direction.RIGHT
        self.alive = True
        self.set_random_fruit_drop()

    def is_alive(self):
        return self.alive

    def button_input(self, button_pressed):
        if button_pressed is ButtonPress.LEFT:
            self.direction = self.direction.pred()
        elif button_pressed is ButtonPress.RIGHT:
            self.direction = self.direction.succ()

    def set_random_fruit_drop(self):
        self.fruit_location = random.choice([x for x in list(range(1, 100)) if x not in self.current_locations])
        print("the fruit location is: " + str(self.fruit_location))

    def check_collision_self(self, location_to_move_to):
        if location_to_move_to in self.current_locations[1:]:
            return True
        else:
            return False

    def check_collision_fruit(self, location_to_move):
        if location_to_move is self.fruit_location:
            return True
        else:
            return False

    def move(self):
        print("current location is:" + self.current_locations.__str__())
        head_pos = self.current_locations[-1]

        if self.direction is Direction.RIGHT:
            if head_pos % 10 == 0:
                move_location = head_pos - 9
            else:
                move_location = head_pos + 1

        elif self.direction is Direction.DOWN:
            if head_pos >= 91:
                move_location = head_pos - 90
            else:
                move_location = head_pos + 10

        elif self.direction is Direction.LEFT:
            if head_pos % 10 == 1:
                move_location = head_pos + 9
            else:
                move_location = head_pos - 1

        elif self.direction is Direction.UP:
            if head_pos <= 10:
                move_location = head_pos + 90
            else:
                move_location = head_pos - 10

        if self.check_collision_self(move_location) is True:
            self.alive = False
            return

        self.current_locations.append(move_location)

        if self.check_collision_fruit(move_location) is True:
            self.set_random_fruit_drop()
        else:
            # moves the tail one step further
            self.current_locations.pop(0)

        print("current positions are" + self.current_locations.__str__())
        


snake = Snake()
print(snake.is_alive())
while snake.is_alive() is False:
    print("Game Over")

while snake.is_alive() is True:
    time.sleep(0.5)
    keyboard_input = input()
    if keyboard_input is "r":
        snake.button_input(ButtonPress.RIGHT)
    elif keyboard_input is "l":
        snake.button_input(ButtonPress.LEFT)
    snake.move()