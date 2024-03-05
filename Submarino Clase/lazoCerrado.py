import pygame
from pygame.locals import *
import sys
import matplotlib.pyplot as plt #Libreria para graficar los desplazamientos
from datetime import datetime, timedelta #Libreria para temporizador

# Variables de tamaño de la pantalla
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 626
# Limite del mar
sea_level = 10
#Variable para darle direccion a la imagen del submarino.
submarine_direction_x = 0  # 0 quieto, -1 izquierda, 1 derecha
# coordenadas de inicio de submarino
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
bx = 32
by = 1

# Clase del tanque donde se controla si el submarino sube o baja segun el volumen del tanque
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

    # Esta es la clase de lazo cerrado con la que se valida la altura a la que debe llegar el submarino
    # La variable target_y es la posicion en y a la que debe llegar el submarino.
    def close_loop(self, positionSubmarine, target_y):
        if positionSubmarine > target_y: #Si el submarino se encuentra en la parte inferior al nivel deseado se le ingresa aire
            self.pumping_air_water("air")
        elif positionSubmarine < target_y: #Si el submarino se encuentra en la parte superior al nivel deseado se le ingresa agua
            self.pumping_air_water("water")
        elif positionSubmarine == target_y: #Si se encuentra en el nivel no hace nada
            print("nada")


# Clase del submarino donde tiene los metodos para calcular el movimiento
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

def main():
    global submarine_direction_x
    pygame.init()
    tank1 = Reservoir(1005, 0.5, 50000, 'air')
    submarine1 = Submarine(tank1, 2, 2,0,150,500)
    target_y = 20
    #Estas dos listas se inicializan para guardar la lista de posiciones y la lista del tiempo para realizar la grafica
    list_time = []
    list_position = []

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Submarine game")

    background_image = pygame.image.load("..\\dinamicos\\Submarino Clase\\fondo.jpeg").convert()
    submarine_image = pygame.image.load("..\\dinamicos\\Submarino Clase\\submarino.jpg").convert_alpha()

    screen.blit(submarine_image, (submarine_image_pos_x, submarine_image_pos_y_init))
    screen.blit(background_image, (0, 0))

    pygame.display.flip()

    #La variable star_time se inicializa con el tiempo real actual, para iniciar el while con un temporizador
    start_time = datetime.now()
    #En end_time se usa para ponerle el limite al temporizador
    end_time = start_time + timedelta(seconds=5)

    #Se cambio el funcionamiento del while y se limita cuando se cumpla el tiempo del temporizador
    while datetime.now() < end_time:
        #La variable current_time se guarda con la hora
        current_time = datetime.now()
        #La hora guardada en el currente_time se resta con el tiempo de inicio y solo se toman los segundos
        #Se hace esto porque de esta forma podemor limitar el temporizador en el tiempo deseado
        elapsed_time = (current_time - start_time).total_seconds()
        #Esos segundos resultantes se guardan en la lista del tiempo para la grafica
        list_time.append(elapsed_time)
        #Se guardan las posiciones del submarino que tenga cada segundo en la lista
        position_submarine = submarine1.pos_y
        list_position.append(position_submarine)

        submarine1.calculate_velocity()
        submarine1.calculate_position()
        submarine1.calculate_position_x()

        screen.blit(background_image, (0, 0))
        screen.blit(submarine_image, (submarine1.pos_x, submarine1.pos_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #Aqui se realiza el evento del mouse.
                    #Se hace uso de la libreria del pygame y el metodo MOUSEBUTTONDOWN con el cual se detecta cuando se hace click
                    #Se guarda en la variable y la posicion del mouse dentro del juego
                    x, y = pygame.mouse.get_pos()
                    #Se guarda el valor en una variable global
                    target_y = y

        submarine1.calculate_mass()
        #Se hace el llamdo al metodo de close_loop y se ingresa como parametro el valor de la posición del submarino y a donde desea llegar
        tank1.close_loop(position_submarine,target_y)

    #Se hace llamado a la libreria de Matplotlib con la cual se puede graficar las lineas de tiempo
    #Se hace con el meto plt.plot, donde se le pasa como parametros cada uno de los ejes tanto el del tiempo como las posiciones
    plt.plot(list_time,list_position)
    #se le da un nombre a cada eje
    plt.xlabel("Position X")
    plt.ylabel("Position Y")

    #Hacemos que la grafica entienda que cada uno de los datos en el eje x y y son uno a uno para que entienda el grafico
    plt.xticks(range(int(min(list_time)), int(max(list_time)) + 1, 1))
    #Se muestra la grafica.
    plt.show()


if __name__ == "__main__":
   submarine_direction_x = 0
   main()