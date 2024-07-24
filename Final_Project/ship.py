import pygame
import math
import numpy as np
class Ship(pygame.sprite.Sprite):
    def __init__(self, screen_width:int, screen_height:int):
        super().__init__()
        self.x,self.y = screen_width/2, screen_height/2
        self.angle = 0 #Angle of ship in degrees where normal is directly North
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.reference_vector = np.array([0, 300])
        self.reference_vector_magnitude = math.sqrt(self.reference_vector[0]**2 + self.reference_vector[1]**2)
        self.new_vector = np.array([self.mouse_x, self.mouse_y])
        self.y_momentum = 0
        self.x_momentum = 0
        self.max_momentum = 5   
        self.distance = 3 #Proportional to distance traveleled in any direction
        self.original_image = pygame.image.load("Png\ship.png").convert()#Image of ship
        self.image = pygame.transform.rotozoom(self.original_image, 0, .2)
        self.image.set_colorkey((0,0,0))
        self.original_circle = pygame.image.load("Png\circle.png").convert_alpha()
        self.circle = pygame.transform.rotozoom(self.original_circle, 0, .1)#Image of bounding circle around mouse
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.index = 1
        self.explosion_image = pygame.image.load(f"Png\ShipExplosion\explosion{int(self.index)}.png").convert_alpha()
        pygame.image.load(f"Png\ShipExplosion\explosion{int(self.index)}.png")

    def check_collision(ship, collide_group):
        """Checks for ship collision with given pygame group"""
        if (pygame.sprite.spritecollide(ship, collide_group,False)):
            sprite = (pygame.sprite.spritecollide(ship, collide_group,False))
            return pygame.sprite.collide_mask(ship, sprite[0])
        
    def move_forward(self):
        """Steps the ship forward proportionally in whatever direction ship is facing and increases momentum"""
        if pygame.Rect.colliderect(self.rect, self.circle_rect) is False:
            self.x += self.distance * math.cos(math.radians(self.angle+90))
            self.y -= self.distance * math.sin(math.radians(self.angle+90))
            self.x_momentum += (math.cos(math.radians(self.angle+90)))/20
            self.y_momentum +=(math.sin(math.radians(self.angle+90)))/20

    def move_backward(self):
        """Moves the ship directly opposite of direction the ship is pointing and increases momentum"""
        self.x += self.distance/2 * math.cos(math.radians(self.angle-90))
        self.y -= self.distance/2 * math.sin(math.radians(self.angle-90))
        self.x_momentum += (math.cos(math.radians(self.angle-90)))/30
        self.y_momentum +=(math.sin(math.radians(self.angle-90)))/30
      
    def move_left(self):
        """Moves Ship left of where ship is facing and increases momentum"""
        self.x+= self.distance/2*math.cos(math.radians(self.angle+180))
        self.y-=self.distance/2*math.sin(math.radians(self.angle+180))
        self.x_momentum += (math.cos(math.radians(self.angle+180)))/60
        self.y_momentum +=(math.sin(math.radians(self.angle+180)))/60
        
    def move_right(self):
        """Moves Ship right of where ship is facing and increases momentum"""
        self.x += self.distance/2 * math.cos(math.radians(self.angle))
        self.y -= self.distance/2 * math.sin(math.radians(self.angle))
        self.x_momentum += (math.cos(math.radians(self.angle)))/60
        self.y_momentum +=(math.sin(math.radians(self.angle)))/60

    def ship_border_check(self):
        """Checks if ship has left the screen and teleports ship to other side of screen if so"""
        if self.rect.midtop[0] <= -100:
            self.x = self.screen_width
        elif self.rect.midtop[0] >= self.screen_width+100:
            self.x = 0
        if self.rect.midtop[1] <= -100:
            self.y = self.screen_height
        elif self.rect.midtop[1] >= self.screen_height+100:
           self.y = 0

    def limit_momentum(self):
        if self.x_momentum >= self.max_momentum:
            self.x_momentum = self.max_momentum

        elif self.x_momentum <= -self.max_momentum:
            self.x_momentum = -self.max_momentum

        if self.y_momentum >= self.max_momentum: 
            self.y_momentum = self.max_momentum

        elif self.y_momentum <= -self.max_momentum:
            self.y_momentum =-self.max_momentum

    def play_death_animation(self, screen):
            while(self.index<9.8):
                self.index+=.1
                pygame.Surface.blit(self.explosion_image, screen, (self.x, self.y))
            return 0 

    def reset_values(self):
        """Resets values of ship to default"""
        self.index = 1
        self.x,self.y = self.screen_width/2, self.screen_height/2
        self.angle = 0 #Angle of ship in degrees where normal is directly North
        self.reference_vector = np.array([0,300])
        self.new_vector = np.array([self.mouse_x-self.x, -1*(self.mouse_y-self.y)])
        self.x_momentum = 0
        self.y_momentum = 0
    
    def update(self):
        """Updates all the ship vector positions, rectangles, angle of ship, and applies momentum to ship"""
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos() 
        self.new_vector = np.array([self.mouse_x-self.x, (self.mouse_y-self.y)*-1])#Converts the mouse vector to regular cartesian coordinates instead of using screen coords
        #Solves for angle between ship and mouse by using identity of dot product between converted vector and the reference vector
        if self.mouse_x < self.x:
            self.angle = math.degrees(math.acos((self.reference_vector.dot(self.new_vector)/(self.reference_vector_magnitude*math.sqrt((self.new_vector[0])**2 + (self.new_vector[1])**2))))) 
        else: 
            self.angle = -1*(math.degrees(math.acos((self.reference_vector.dot(self.new_vector)/(self.reference_vector_magnitude*math.sqrt((self.new_vector[0])**2 + (self.new_vector[1])**2))))))
        self.x+= self.x_momentum*self.distance
        self.y -= self.y_momentum *self.distance
        self.limit_momentum()
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, .15).convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.circle_rect = self.circle.get_rect(center =(self.mouse_x, self.mouse_y))# Rect for limiting circle drawn around mouse to avoid glitching when holding W near the mouse
        self.ship_border_check()
       
