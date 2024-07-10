import pygame
import math

import pygame.surface

class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship_x, ship_y, ship_angle):
        super().__init__()
        self.velocity = 10
        self.x = ship_x
        self.y = ship_y
        self.angle = ship_angle
        self.original_image = pygame.image.load("bullet2.png")
        self.image =pygame.transform.rotozoom(self.original_image, self.angle+90, .25)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.wait_frames = 5
        self.collision = False
     
    
    def destroy(self):
        """Checks if bullet has left the screen. If so destroys the bullet"""
        if self.x >= 1100 or self.x <= -100:
            self.kill()
            return None
        elif self.y >= 900 or self.y <= -100:
            self.kill()
            return None

    def update(self, group):
        """Handles collision of bullet and asteroid. Removes both bullet and asteroid on collision after waiting self.wait_frames amount of frames"""
        if pygame.sprite.spritecollideany(self, group) != None:
            self.collision = True
            self.collision_sprite = pygame.sprite.spritecollideany(self, group)
        if self.collision:
            self.wait_frames-=1
            if self.wait_frames <=0:
                pygame.sprite.Sprite.kill(self)
                pygame.sprite.Sprite.kill(self.collision_sprite)
        self.x += self.velocity * math.cos(math.radians(self.angle+90)) 
        self.y -= self.velocity * math.sin(math.radians(self.angle+90))
        self.rect = self.image.get_rect(center = (self.x, self.y))  
        self.destroy()
        
        
       
     