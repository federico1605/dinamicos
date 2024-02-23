import pygame
from pygame.locals import *
import sys

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 626
sea_level = 10
submarine_direction_x = 0  # 0 quieto, -1 izquierda, 1 derecha
submarine_image_pos_x = 500
submarine_image_pos_yLim = 500
submarine_image_pos_xLim = 900
submarine_image_pos_y_init = sea_level

g = 9.8 # Gravity constant
p = 1000  # Fluid density  1000 m^3/kg for water
v = 1  # Robot total volume
dt = 1  # Delta time. It depends on CPU clock frequency and computational complexity
b = 250 # Friction constant
e = - (p * g * v) # Buoyancy
fep = 30 # Fuerza de propulsion cohete
fe= 100
bx = 32
by = 1

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



class Submarine:
   def __init__(self, tank, mass, actual_velocity, pushing_force, pos_y, pos_x):
       self.pos_x = pos_x
       self.pos_y = pos_y
       self.mass = mass
       self.actual_velocity = actual_velocity
       self.pushing_force = pushing_force
       self.tank = tank
       self.direction = 1

   def calculate_mass(self):
       self.mass = self.tank.actual_level

   def calculate_velocity(self):
       self.actual_velocity = dt * ((e / self.mass) + g - ((b * self.actual_velocity) / self.mass)) + self.actual_velocity

   def calculate_velocity_x(self):
       self.pushing_force = (dt * (self.pushing_force - b )) /self.mass + self.pushing_force

   def calculate_position_x(self):
        self.pos_x += self.pushing_force

   def curb_submarine(self):
        self.pushing_force = 0

   def calculate_position(self):
       self.pos_y = self.pos_y + self.actual_velocity

       if self.pos_y > submarine_image_pos_yLim:
           self.pos_y = submarine_image_pos_yLim

       if  self.pos_y < sea_level:
           self.pos_y = sea_level

       if  self.pos_x > submarine_image_pos_xLim:
           self.pos_x = submarine_image_pos_xLim

       if self.pos_x < sea_level:
           self.pos_x = sea_level
       return self.pos_y, self.pos_x

   def set_direction(self, direction):
        self.direction = direction

class Torpedo:
    def __init__(self, speed_x, speed_y, pos_y_torpedo, pos_x_torpedo, mass_torpedo, image_right, image_left, direction_torpedo):
       self.pos_x_torpedo = pos_x_torpedo
       self.pos_y_torpedo = pos_y_torpedo
       self.speed_x = speed_x * -direction_torpedo
       self.speed_y = speed_y
       self.mass_torpedo = mass_torpedo
       self.image_right = image_right
       self.image_left = image_left
       self.image = image_right if direction_torpedo == -1 else image_left

    def calculate_speed_y(self):
        self.speed_y = (dt * ((e/self.mass_torpedo) + g - ((by * self.speed_y) / self.mass_torpedo))) + self.speed_y

    def calculate_speed_x(self):
        self.speed_x = (dt * (((fep - bx) * self.speed_x) / self.mass_torpedo)) + self.speed_x

def main():
   global submarine_direction_x
   pygame.init()
   tank1 = Reservoir(1005, 2, 50000, 'air')
   submarine1 = Submarine(tank1, 2, 2,0,150,500)
   torpedos = []

   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

   pygame.display.set_caption("Submarine game")

   background_image = pygame.image.load("..\\dinamicos\\Submarino Clase\\fondo.jpeg").convert()
   submarine_image = pygame.image.load("..\\dinamicos\\Submarino Clase\\submarino.jpg").convert_alpha()
   original_submarine_image = submarine_image
   torpedo_img = pygame.image.load("..\\dinamicos\\Submarino Clase\\torpedo.png").convert_alpha()
   projectile_image_left = pygame.transform.flip(torpedo_img, True, False)

   screen.blit(submarine_image, (submarine_image_pos_x, submarine_image_pos_y_init))
   screen.blit(background_image, (0, 0))

   pygame.display.flip()

   while True:
       submarine1.calculate_velocity()
       submarine1.calculate_position()
       submarine1.calculate_position_x()

       screen.blit(background_image, (0, 0))
       screen.blit(submarine_image, (submarine1.pos_x, submarine1.pos_y))

       for torpedo in torpedos:
            torpedo.calculate_speed_x()
            torpedo.calculate_speed_y()
            print(torpedo.speed_y)
            torpedo.pos_x_torpedo += torpedo.speed_y
            torpedo.pos_y_torpedo += torpedo.speed_x
            screen.blit(torpedo.image, (torpedo.pos_y_torpedo,torpedo.pos_x_torpedo))

       pygame.display.flip()

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               sys.exit()
           elif event.type == pygame.KEYDOWN:
               if event.key == K_UP:
                   tank1.pumping_air_water('air')

               elif event.key == K_DOWN:
                   tank1.pumping_air_water('water')

               elif event.key == pygame.K_LEFT:  # Flecha izquierda
                    submarine_image = original_submarine_image
                    submarine_direction_x = 1
                    submarine1.set_direction(submarine_direction_x)
                    submarine1.calculate_velocity_x()

               elif event.key == pygame.K_RIGHT:  # Flecha derecha
                    submarine1.pushing_force += 0.5
                    submarine1.calculate_velocity_x()
                    submarine_image = pygame.transform.flip(original_submarine_image, True, False)
                    submarine_direction_x = -1
                    submarine1.set_direction(submarine_direction_x)

               elif event.key == pygame.K_SPACE:
                    submarine1.curb_submarine()

               elif event.key == pygame.K_a:
                  new_torpedo = Torpedo(1, 0.3, submarine1.pos_x, submarine1.pos_y, 1000, torpedo_img, projectile_image_left, submarine1.direction)

                  torpedos.append(new_torpedo)


       submarine1.calculate_mass()

if __name__ == "__main__":
   submarine_direction_x = 0
   main()