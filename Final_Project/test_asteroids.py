import pygame
import random
import numpy as np
import math
from ship import Ship

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,screen_height, screen_width, wave):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        #Dict of the ranges the asteroid can spawn in relation to the screen
        self.spawn_ranges = {
            "top" :[(0,screen_width),(-100,0)],
            "bottom":[(0,screen_width), (screen_height, screen_height+100)],
            "left": [(-100, 0), (0,screen_height )],
            "right": [(screen_width, screen_width+100), (0, screen_height)]
        }
        self.choice=random.choice(("top", "bottom", "left", "right"))#Randomly choosing one of the dict keys
        self.velocity  = 5*wave
        self.x = random.randrange(self.spawn_ranges[self.choice][0][0],self.spawn_ranges[self.choice][0][1] )#Randomly initializing x-value based on the random choice of ranges
        self.y = random.randrange(self.spawn_ranges[self.choice][1][0],self.spawn_ranges[self.choice][1][1] )#Randomly initializing y-value based on the random choice of ranges
        self.point = [0,0]
        
        self.reference_vector = np.array([-(self.x-screen_width/2), 400])
        self.reference_vector_magnitude = math.sqrt(self.reference_vector[0]**2 + self.reference_vector[1]**2)
        #self.point = [random.randrange((screen_width/2-300)-screen_width/2, screen_width/2+300-screen_width/2), random.randrange(screen_height/2-100+screen_width/2,screen_height/2+100+screen_width/2)]#Generates a random point within screen to determine direction of asteroid based on the cartesian plane
        self.vector = np.array([self.point[0]-(self.x-screen_width/2), self.point[1]-(screen_height/2-self.y)])
        
        if self.choice =="left":
            self.angle =  90-math.degrees(math.acos((self.reference_vector.dot(self.vector)/(self.reference_vector_magnitude*math.sqrt((self.vector[0])**2 + (self.vector[1])**2))))) 
        elif self.choice == "top" and self.point[0]>self.x:
            self.angle =  90-math.degrees(math.acos((self.reference_vector.dot(self.vector)/(self.reference_vector_magnitude*math.sqrt((self.vector[0])**2 + (self.vector[1])**2))))) 
        else:
            self.angle = 90+math.degrees(math.acos((self.reference_vector.dot(self.vector)/(self.reference_vector_magnitude*math.sqrt((self.vector[0])**2 + (self.vector[1])**2))))) 
        self.image = pygame.transform.rotozoom(self.image, 90, .1)
        self.x_spawn = self.x 
        self.y_spawn =self.y
    
    def destroy(self):
        if self.x >= 1100 or self.x <= -100:
            self.kill
            return None
        elif self.y >= 900 or self.y <= -100:
            self.kill
            return None
        
    def draw_asteroid(self):
        #draw the asteroid and define rect
        self.rect = self.image.get_rect(center = (self.x, self.y))
    def update(self):
        print(self.point, self.vector, self.x_spawn, self.y_spawn)
        self.draw_asteroid()
        self.x += self.velocity*math.cos(math.radians(self.angle))
        self.y += self.velocity*math.sin(math.radians(self.angle))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.destroy()
        