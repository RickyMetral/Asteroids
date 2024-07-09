import pygame
import math
import numpy as np
class Ship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.x,self.y = screen_width/2, screen_height/2
        self.angle = 0 #Angle of ship in degrees where normal is directly North
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.reference_vector = np.array([0, 300])
        self.reference_vector_magnitude = math.sqrt(self.reference_vector[0]**2 + self.reference_vector[1]**2)
        self.new_vector = np.array([self.mouse_x, self.mouse_y])
        self.y_momentum = 0
        self.x_momentum = 0
        self.distance = 3 #Proportional to distance traveleled in any direction
        self.orignal_image = pygame.image.load("ship.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.orignal_image, 0, .2)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.screen_width = screen_width
        self.screen_height =screen_height
         
    def move_forward(self):
        """Steps the ship forward proportionally in whatever direction ship is facing and increases momentum"""
        self.x += self.distance * math.cos(math.radians(self.angle+90))
        self.y -= self.distance * math.sin(math.radians(self.angle+90))
       
    def move_backward(self):
        """Moves the ship directly opposite of direction the ship is pointing and increases momentum"""
        self.x += self.distance/2 * math.cos(math.radians(self.angle-90))
        self.y -= self.distance/2 * math.sin(math.radians(self.angle-90))
      
        # if self.rect.x <= 0:
        #     self.x=0
        # if self.rect.y <=0:
        #     self.y = 0
        # elif self.rect.x >= self.screen_width:
        #     self.x= self.screen_width
        # elif self.rect.y >=self.screen_height:
        #     self.y= self.screen_height

    def move_left(self):
        """Moves Ship left of where ship is facing and increases momentum"""
        self.x += self.distance/3 * math.cos(math.radians(self.angle+180))
        self.y -= self.distance/3 * math.sin(math.radians(self.angle+180))
        # self.x_momentum += (math.cos(math.radians(self.angle+90)))/10
        # self.y_momentum -=(math.sin(math.radians(self.angle+90)))/10
        
    def move_right(self):
        """Moves Ship right of where ship is facing and increases momentum"""
        self.x += self.distance/3 * math.cos(math.radians(self.angle))
        self.y -= self.distance/3 * math.sin(math.radians(self.angle))
        # self.x_momentum += (math.cos(math.radians(self.angle+90)))/10
        # self.y_momentum -=(math.sin(math.radians(self.angle+90)))/10

    def ship_border_check(self):
        if self.rect.midtop[0] <=-100:
            self.x = self.screen_width
        elif self.rect.midtop[0] >= self.screen_width+100:
            self.x = 0
        if self.rect.midtop[1] <=-100:
            self.y = self.screen_height
        elif self.rect.midtop[1] >= self.screen_height+100:
           self.y = 0
        

    def reset_values(self):
        """Resets values of ship to default """
        self.x,self.y = self.screen_width/2, self.screen_height/2
        self.angle = 0 #Angle of ship in degrees where normal is directly North
        self.reference_vector = np.array([0,300])
        self.new_vector = np.array([self.mouse_x-self.x, -1*(self.mouse_y-self.y)])
        self.x_momentum = 0
        self.y_momentum = 0
    
    def update(self):
        """Updates all the ship vector positions, rectangles, and angle of ship"""    
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos() 
        self.new_vector = np.array([self.mouse_x-self.x, (self.mouse_y-self.y)*-1])#Converts the mouse vector to regular cartesian coordinates instead of using screen coords
        #Solves for angle between ship and mouse by using identity of dot product between converted vector and the reference vector
        if self.mouse_x < self.x:
            self.angle = math.degrees(math.acos((self.reference_vector.dot(self.new_vector)/(self.reference_vector_magnitude*math.sqrt((self.new_vector[0])**2 + (self.new_vector[1])**2))))) 
        else: 
            self.angle = -1*(math.degrees(math.acos((self.reference_vector.dot(self.new_vector)/(self.reference_vector_magnitude*math.sqrt((self.new_vector[0])**2 + (self.new_vector[1])**2))))))
        self.image = pygame.transform.rotozoom(self.orignal_image, self.angle, .15)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        print(self.rect.topleft, self.rect.bottomleft)
      
    
