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



# ------------------------------

# Main function

# ------------------------------

def main():

   pygame.init()

   submarine_image_pos_y=150

   # --------------------------------------------

   # Creation of the window and assigning a title

   # --------------------------------------------

   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

   pygame.display.set_caption("Submarine game")

   # -----------------------------------------

   # Load images (creation of Surface objects)

   # -----------------------------------------

   background_image = pygame.image.load("E:\Dinamicos\Submarino Clase\mar.jpg").convert()

   #Some image formats needs alpha conversion

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

       #Increases the distance measured from sea level, due to the permanent action of gravity

       # -------------------------------------------------------------------------------------

       submarine_image_pos_y = submarine_image_pos_y + 1

       # -----------------------------------------------------------------

       #Verify that the actual position isn´t greater than the screen edge

       # -----------------------------------------------------------------

       if submarine_image_pos_y > submarine_image_pos_yLim:

           submarine_image_pos_y = submarine_image_pos_yLim

       # --------------------------------------------

       #place Images onto screen

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

                   submarine_image_pos_y = submarine_image_pos_y - 100

               elif event.key == K_DOWN:

                   submarine_image_pos_y = submarine_image_pos_y + 100



if __name__ == "__main__":

   main()