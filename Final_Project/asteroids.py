

import pygame
import random
import numpy as np
import math
from ship import Ship

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,screen_height, screen_width, wave, ship_x, ship_y):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.velocity  = 5*math.log(wave+1)
        self.screen_width = screen_width
        self.screen_height = screen_height

        #Dict of the ranges the asteroid can spawn in relation to the screen
        self.spawn_ranges = {
            "top" :[(0,screen_width),(-100,0)],
            "bottom":[(0,screen_width), (screen_height, screen_height+100)],
            "left": [(-100, 0), (0,screen_height )],
            "right": [(screen_width, screen_width+100), (0, screen_height)]
        }
        self.choice=random.choice(("top", "bottom", "left", "right"))#Randomly choosing one of the dict keys
        self.x = random.randrange(self.spawn_ranges[self.choice][0][0],self.spawn_ranges[self.choice][0][1] )#Randomly initializing x-value based on the random choice of ranges
        self.y = random.randrange(self.spawn_ranges[self.choice][1][0],self.spawn_ranges[self.choice][1][1] )#Randomly initializing y-value based on the random choice of ranges
        self.point = np.array([random.randrange(int(ship_x-150), int(ship_x+150)), random.randrange(int(ship_y-150),int(ship_y+150))])#
        self.distance = math.sqrt((self.point[0]-self.x)**2 + (self.point[1]-self.y)**2)
        self.vector =np.array([(self.point[0]-self.x), (self.point[1]-self.y)])
        self.image = pygame.transform.rotozoom(self.image, 90, .1)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.point[0] += 5*self.vector[0]
        self.point[1] += 5*self.vector[1]

 
    def destroy(self):
        """Checks and destroys asteroid if too far out of screen bounds"""
        if self.x >= 1100 or self.x <= -100:
            self.kill()
            return None
        elif self.y >= 900 or self.y <= -100:
            self.kill()
            return None
        
   
    def update(self):
        """Updates the position of the asteroid and moves endpoint further if asteroid gets too close"""
       
        self.distance = math.sqrt((self.point[0]-self.x)**2 + (self.point[1]-self.y)**2)
        self.x+= self.velocity*(self.point[0]-self.x)/self.distance
        self.y+= self.velocity*(self.point[1]-self.y)/self.distance
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.destroy()
        

