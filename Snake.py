# Snake game
# 10x10 RGB LED Matrix "Snake" game


#===========================================================================================================#

#SCRAPPED VERSIONS OF FUNCTIONS IN CASE UPDATED VERSIONS CREATE ERRORS:

#----------------------scrapped because wrong--------------------------#
#def random_fruit_drop(snake_body_length, recent_100):                 #                
#    possible_fruit_cell = recent_100[:-snake_body_length]             #                
#    random_position = random.randint(0,len(possible_fruit_cell)-1)    #                
#    return possible_fruit_cell[random_position]                       #                
#----------------------------------------------------------------------#

#-----------scrapped because too complicated for no reason-------------#
#def check_collision(all_snake_positions, head_pos):                   #                     
#    for i in enumerate(all_snake_positions):                          #                                                           
#        if i == len(all_snake_positions):                             #
#            break                                                     #
#        elif all_snake_positions[i] == head_pos:                      #  
#            alive = False                                             #
#        else:                                                         #
#            pass                                                      #
#----------------------------------------------------------------------#

#===========================================================================================================#

# LED strip configuration:
LED_COUNT      = 100     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels 
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz 
LED_DMA        = 5       # DMA channel to use for generating signal 
LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
# LED strip configuration\

import random
import time

alive = True 
head_pos = 42                                                                           #starting point at LED #42, obviously.
direction = 0                                                                           #starting direction is moving from left to right
fruit_location = 44

snake_body_length = 1                                                                   #lenght of the snakes body in pixels, also amount of fruit eaten -1
recent_100 = []
for i in range (1,42):
    recent_100.append(i)
for i in range (43,101):
    recent_100.append(i)
recent_100.append(42)                                                                  #adding all values from 1-100 with 42 being the last one added
                                                                      

all_snake_positions = []

#def check_everything(recent_100,snake_body_length,all_snake_positions,head_pos):
# 
#    if len(recent_100) >= 100:                                                          #----------------------------------ADJUST RECENT_100:------------------------------------------                                                    
#        recent_100.pop(0)
#    else:
#        pass
#    recent_100.append(head_pos)
#  
#    all_snake_positions = recent_100[-snake_body_length:]                               #give positions of all parts of the snake
#
#    if head_pos in all_snake_positions[0:snake_body_length-1]:                          #----------------------------------CHECKING COLLISION:-----------------------------------------
#        alive = False
#    else:
#        pass
#                                                                                                                                                                                   
#    if head_pos == fruit_location:                                                      #---------------------------------CHECKING IF FRUIT IS DEVOURED:-------------------------------
#        snake_body_length += 1                                                          #if the head of the snake matches the random fruit drop, increase lenght by one
#        all_snake_positions = recent_100[-snake_body_length:]                           #update the snake to actually make it one pixel longer
#        random_fruit_drop(snake_body_length,recent_100)                                 #create new fruit drop
#    else:       
#        pass
#    return snake_body_length, all_snake_positions    
    
        
def random_fruit_drop(snake_body_length,recent_100):                                    #function to spawn fruit on a non-occupied pixel                       
    fruit_location = random.randint(1,100)                                              #creates a random value between 1 and 100
    while fruit_location in recent_100[-snake_body_length:]:                            #repeats until that value is not matching with any of the values in "all_snake_positions"
        fruit_location = random.randint(1,100)
    return fruit_location

def check_body_length(recent_100):
    if len(recent_100) >= 100:                                                          #checking if the list is full (100+)
        recent_100.pop(0)                                                               #if so, erasing first entry
    recent_100.append(head_pos)                                                         #adding current position to recent list

def increase_body_length(recent_100,snake_body_length):                                 #adding the other pixels to the snake body
    all_snake_positions = recent_100[-snake_body_length:]
    return all_snake_positions                                                          #giving out a list of all positions 

def check_collision(all_snake_positions, head_pos):                                     #checks if the snake collides with itself, resulting in a game over                                
    if head_pos in all_snake_positions[0:snake_body_length-1]:                          #this is done by comparing the current head position with the array of all snake positions except the last one (head_pos itself)
        alive = False                                                                   #if that position is in there already, it means the snake has crossed paths with itself.
    else:
        pass

print(alive)

random_fruit_drop(snake_body_length,recent_100)
print(fruit_location) 

while alive == False:

    print("Game Over") 

while alive == True:
    
    if direction == 0:                                                                  #from left to right (starting direction)
        keyboard_input = input()
        if keyboard_input == "r": #change this to "while button_r = True"
            if head_pos >= 91:                            
                head_pos = head_pos - 90
                time.sleep(0.2)                
                check_body_length(recent_100)
                increase_body_length(recent_100,snake_body_length)
                direction = 1
            else:                           
                head_pos = head_pos + 10
                time.sleep(0.2)               
                check_body_length(recent_100)
                increase_body_length(recent_100,snake_body_length)
                direction = 1

        elif keyboard_input == "l":
            if head_pos <= 10:
                head_pos = head_pos + 90
                time.sleep(0.2)                
                check_body_length(recent_100)
                direction = 3
            else:
                head_pos = head_pos - 10
                time.sleep(0.2)
                check_body_length(recent_100)
                direction = 3
        
        else:
            if head_pos % 10 == 0:
                head_pos = head_pos - 9         
                time.sleep(0.2)                
                check_body_length(recent_100) 
            else:
                head_pos += 1
                time.sleep(0.2)                
                check_body_length(recent_100)

    if direction == 1:                                                                       #from top to bottom 
        keyboard_input = input()
        if keyboard_input == "r":
            if head_pos %10 == 1:
                head_pos = head_pos + 9
                time.sleep(0.2)                
                check_body_length(recent_100)
                direction = 2
            else:
                head_pos = head_pos - 1
                time.sleep(0.2)                
                check_body_length(recent_100)
                direction = 2

        elif keyboard_input == "l":
            if head_pos % 10 == 0:
                head_pos = head_pos - 9
                time.sleep(0.2)                
                check_body_length(recent_100) 
                direction = 0
            else:
                head_pos = head_pos + 1
                time.sleep(0.2)                
                check_body_length(recent_100)
                direction = 0

        else:
            if head_pos >= 91:
                head_pos = head_pos - 90         
                time.sleep(0.2)                
                check_body_length(recent_100)
            else:
                head_pos = head_pos + 10
                time.sleep(0.2)                
                check_body_length(recent_100) 

    if direction == 2:                                                                       #from right to left 
        keyboard_input = input()
        if keyboard_input == "r":
            if head_pos <=10:
                head_pos = head_pos + 90
                time.sleep(0.2)               
                check_body_length(recent_100)
                direction = 3
            else:
                head_pos = head_pos - 10
                time.sleep(0.2)                
                check_body_length(recent_100) 
                direction = 3

        elif keyboard_input == "l":
            if head_pos >=91:
                head_pos = head_pos - 90
                time.sleep(0.2)                
                check_body_length(recent_100) 
                direction = 1
            else:
                head_pos = head_pos + 10
                time.sleep(0.2)                
                check_body_length(recent_100) 
                direction = 1

        else:
            if head_pos %10 == 1:
                head_pos = head_pos + 9         
                time.sleep(0.2)                
                check_body_length(recent_100) 
            else:
                head_pos = head_pos - 1
                time.sleep(0.2)                
                check_body_length(recent_100) 

    if direction == 3:                                                                      #from bottom to top
        keyboard_input = input()
        if keyboard_input == "r":
            if head_pos %10 == 0:
                head_pos = head_pos - 9
                time.sleep(0.2)                
                check_body_length(recent_100) 
                direction = 0
            else:
                head_pos = head_pos +1
                time.sleep(0.2)                
                check_body_length(recent_100) 
                direction = 0

        elif keyboard_input == "l":
            if head_pos %10 == 1:
                head_pos = head_pos + 9
                time.sleep(0.2)                
                check_body_length(recent_100) 
                direction = 2
            else:                
                head_pos = head_pos - 1
                time.sleep(0.2)               
                check_body_length(recent_100) 
                direction = 2

        else:
            if head_pos <=10:                
                head_pos = head_pos + 90        
                time.sleep(0.2)                
                check_body_length(recent_100)                 
            else:               
                head_pos = head_pos - 10
                time.sleep(0.2)                
                check_body_length(recent_100) 