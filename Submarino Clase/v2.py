import pygame

from pygame.locals import *

import sys


# -----------

# Constants

# -----------

SCREEN_WIDTH = 1000

SCREEN_HEIGHT = 785

sea_level = 150

submarine_image_pos_x = 500

submarine_image_pos_yLim = 500

submarine_image_pos_y_init = sea_level



# ------------------------------

# Classes and Functions

# ------------------------------


class Reservoir:

   def __init__(self, actual_level, valve_flow, max_capacity, fluid_to_pump):

       self.actual_level = actual_level

       self.valve_flow = valve_flow

       self.max_capacity = max_capacity

       self.fluid_to_pump = fluid_to_pump


   def pumping_air_water(self, fluid_to_pump):

       if fluid_to_pump == 'air':

           if self.actual_level > 0:

               self.actual_level = self.actual_level - self.valve_flow

           else:

               self.actual_level = 0

       if fluid_to_pump == 'water':

           if self.actual_level < self.max_capacity:

               self.actual_level = self.actual_level + self.valve_flow

           else:

               self.actual_level = self.max_capacity


# ------------------------------

# Main function

# ------------------------------

def main():

   pygame.init()

   tank1 = Reservoir(500, 2, 100000 , 'air')

   submarine_image_pos_y = 150

   # --------------------------------------------

   # Creation of the window and assigning a title

   # --------------------------------------------

   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

   pygame.display.set_caption("Submarine game")

   # -----------------------------------------

   # Load images (creation of Surface objects)

   # -----------------------------------------

   background_image = pygame.image.load("E:\Dinamicos\Submarino Clase\mar.jpg").convert()

   # Some image formats needs alpha conversion

   submarine_image = pygame.image.load("E:\Dinamicos\Submarino Clase\sub.jpg").convert_alpha()

   # --------------------------------------------

   # The blit method place images onto screen

   # We specify the position of the 'Surface' on the window

   # --------------------------------------------

   screen.blit(submarine_image, (submarine_image_pos_x, submarine_image_pos_y_init))

   screen.blit(background_image, (0, 0))

   # --------------------------------------------

   # Displaying changes on the screen

   # --------------------------------------------

   pygame.display.flip()


   # Main loop

   while True:

       # -------------------------------------------------------------------------------------

       # Increases the distance measured from sea level, due to the permanent action of gravity

       # -------------------------------------------------------------------------------------

       submarine_image_pos_y = submarine_image_pos_y + 1

       # -----------------------------------------------------------------

       # Verify that the actual position isn´t greater than the screen edge

       # -----------------------------------------------------------------

       if submarine_image_pos_y > submarine_image_pos_yLim:

           submarine_image_pos_y = submarine_image_pos_yLim

       # --------------------------------------------

       # place Images onto screen

       # --------------------------------------------

       screen.blit(background_image, (0, 0))

       screen.blit(submarine_image, (submarine_image_pos_x, submarine_image_pos_y))

       # --------------------------------------------

       # Re-draw all elements

       # --------------------------------------------

       pygame.display.flip()

       # --------------------------------------------

       # Possible mouse and keyboard inputs

       # --------------------------------------------

       for event in pygame.event.get():

           if event.type == pygame.QUIT:

               sys.exit()

           elif event.type == pygame.KEYDOWN:

               if event.key == K_UP:

                   tank1.pumping_air_water('air')

               elif event.key == K_DOWN:

                   tank1.pumping_air_water('water')

       submarine_image_pos_y =tank1.actual_level


if __name__ == "__main__":

   main()

