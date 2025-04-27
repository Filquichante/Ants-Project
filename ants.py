
# import the pygame module
import pygame
import math
import random

pygame.init()
pygame.display.init()
clock = pygame.time.Clock()


all_ants_list = pygame.sprite.Group()
all_pheromone_list = pygame.sprite.Group()



# GLOBAL VARIABLES
aspect_ratio = 16 / 9 
WIDTH = 1540
HEIGHT = 865

# Define the background colour
# using RGB color coding.
background_colour = ("#113366")
  
# Define the dimensions of
# screen object(width,height)
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)


def calculate_new_xy(old_xy, vitesse, angle):
        new_x = (old_xy[0] + math.cos(math.radians(angle)) * vitesse)%WIDTH
        new_y = (old_xy[1] - math.sin(math.radians(angle)) * vitesse)%HEIGHT
        return new_x, new_y


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect


def alea_rotate(sprite, intensity):    
    sprite.rotate(random.randint(0,2*intensity)-intensity)
    sprite.update(3, sprite.angle)
    

def updatePheromone():
    global all_pheromone_list

    for pheromone in all_pheromone_list.sprites():
        pheromone.alpha -= 2  # Diminuer progressivement l'opacité
        if pheromone.alpha <= 0:
            all_pheromone_list.remove(pheromone)  # Supprimer la phéromone du groupe si l'opacité est inférieure ou égale à 0
        else:
            pheromone.surface.fill("white")
            pheromone.surface.set_alpha(pheromone.alpha)  # Définir l'opacité de la surface
            screen.blit(pheromone.surface, pheromone.rect.topleft)  # Dessiner la phéromone à sa position





#######################
# Classe de la fourmi #
#######################



class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y,height, width):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([1,1])
        self.image.fill(color)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image.set_colorkey("white")
        self.rotated_image = self.image
        self.image_propre = self.image
        self.speed = 5
        self.max_rotation = 20
        self.angle = 0
        self.rect = self.rotated_image.get_rect()
        self.rect.center=(x,y)

    def update(self, speed, direction):
        self.rect.center=calculate_new_xy(self.rect.center,speed,direction)
        self.put_pheromone()

    def rotate(self, angle):
        self.angle += angle
        self.rotated_image, self.rect = rot_center(self.image_propre, self.angle, self.rect.center[0], self.rect.center[1])
        self.image = self.rotated_image
        self.rect = self.rotated_image.get_rect(center=self.rect.center)
        self.rect.width = self.rotated_image.get_width()
        self.rect.height = self.rotated_image.get_height()

    def put_pheromone(self):
        pheromone = Pheromone(self.rect.center[0], self.rect.center[1], 255)
        all_pheromone_list.add(pheromone)

    def reach(self, goal_pos:list):    
        ### Tout d'abord, on s'occupe d'aller le bon sens x
        
        
        real_goal_pos = [0, 0]
        goal_x = goal_pos[0]
        goal_y = goal_pos[1]

        if self.rect.center[0] > goal_x:                    # Goal |     |     |     | Self
            if self.rect.center[0] - goal_x > goal_x + WIDTH - self.rect.center[0]: # Goal |     |     |     | Self | Goal2
                real_goal_pos[0] = goal_x + WIDTH
            else:                                                                   # Goal |     | Self |     |     |Goal2
                real_goal_pos[0] = goal_x
        else:                                               # Self |     |     |     | Goal
            if goal_x - self.rect.center[0] < self.rect.center[0] + WIDTH - goal_x: #  Goal 2|     |     | Self |     | Goal 
                real_goal_pos[0] = goal_x
            else:                                                                   #  Goal 2|     | Self |     |     | Goal 
                real_goal_pos[0] = goal_x - WIDTH
        


        #Maintenant on fait le y, c'est très semblable (heureusement lol)        

        if self.rect.center[1] > goal_y:                    # Goal |     |     |     | Self
            if self.rect.center[1] - goal_y > goal_y + HEIGHT - self.rect.center[1]: # Goal |     |     |     | Self | Goal2
                real_goal_pos[1] = goal_y + HEIGHT
            else:                                                                   # Goal2 | Goal |     |     |     | Self
                real_goal_pos[1] = goal_y
        else:                                               # Self |     |     |     | Goal
            if goal_y - self.rect.center[1] < self.rect.center[1] + HEIGHT - goal_y: #  Goal 2|     |     | Self |     | Goal 
                real_goal_pos[1] = goal_y
            else:                                                                   #  Goal 2|     | Self |     |     | Goal 
                real_goal_pos[1] = goal_y - HEIGHT

        #real_goal_pos = goal_pos  #Pour un test tkt

        angle_ideal_radians = math.atan2(0 - real_goal_pos[1] + self.rect.center[1], real_goal_pos[0] - self.rect.center[0])
        angle__ideal_degrees = math.degrees(angle_ideal_radians)
        #self.angle = angle__ideal_degrees
        da = (angle__ideal_degrees - self.angle)%360            #delta_angle = difference between the ideal angle and the real one

        if da > 360 - self.max_rotation :
            self.rotate(0 - da)

        elif da >= 180:
            self.rotate(0 - self.max_rotation)

        elif da < 180:
            self.rotate(self.max_rotation)

        elif da < self.max_rotation:
            self.rotate(da)

        sprite.update(self.speed, sprite.angle)




#############
# Phéromone #
#############

class Pheromone(pygame.sprite.Sprite):
    def __init__(self, x, y, alpha):
        super().__init__()
        self.surface = pygame.Surface((1, 1))
        self.rect = self.surface.get_rect()
        self.rect.center = (x, y)
        self.alpha = alpha



### Création des fourmis

for j in range(0, WIDTH, int(WIDTH/2)):
    for i in range(0, HEIGHT, int(HEIGHT/10)):
        ant = Sprite("red", WIDTH/2+j, HEIGHT/2+i, 1,1)    
        all_ants_list.add(ant)

len_list = len(all_ants_list)
sprites_list = all_ants_list.sprites()  # Convertir l'objet "Group" en une liste de sprites
random.shuffle(sprites_list)


  
# Set the caption of the screen
pygame.display.set_caption('Ants/Slime following each other')
pygame_icon = pygame.image.load("C:\\Users\\Filquichante\\OneDrive\\Bureau\\Ants\\logo.png")
pygame.display.set_icon(pygame_icon)
pygame.display.set_mode((0,0), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
  
# Fill the background colour to the screen
screen.fill(background_colour)
  
# Update the display using flip
pygame.display.flip()
  







# Variable to keep our game loop running
running = True
count_move = 100
for sprite in all_ants_list:
    sprite.rotate(random.randint(0,360))
    sprite.update(5, sprite.angle)



# game loop
while running:
    count_move -= 1
    mouse_pos = pygame.mouse.get_pos()


    # for loop through the event queue
    for event in pygame.event.get():      
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                running = False

        '''elif event.type == pygame.VIDEORESIZE:
            # Gérer le redimensionnement de la fenêtre
            width, height = event.w, event.h
            # Recalculer la largeur en fonction du ratio
            if width==event.wt:
                height = event.h
                width = int(height * aspect_ratio)
            else:
                width = event.w
                height = int(width * aspect_ratio)
            screen = pygame.display.set_mode((width, height), flags)
            screen.fill(background_colour)
            pygame.display.update()'''                                  #Si jamais je veux redimensionner l'écran, mais c'est casse-pieds donc on verra plus tard
    
    screen.fill(background_colour)



    for index, sprite in enumerate(sprites_list):
        sprite.reach(sprites_list[(index+1) % len_list].rect.center)




    
    updatePheromone()

    all_ants_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
