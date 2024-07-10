import pygame
from sys import exit
from ship import Ship
from bullet import Bullet
from asteroids import Asteroid
import math


screen_width = 1000
screen_height = 800
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Asteroids!")
clock = pygame.time.Clock()
ship1 = Ship(screen_width, screen_height)
ship_group = pygame.sprite.Group()
ship_group.add(ship1)
asteroid_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
ASTEROID_SPAWN = pygame.event.custom_type()
NEW_WAVE_EVENT = pygame.event.custom_type()
NEW_WAVE_END = pygame.event.custom_type()
BEGIN_NEW_WAVE = pygame.event.custom_type()
font_index = 0

def main():
    """Controls:  
    W: Accelerate
    S: Decelerate
    A: Move Left
    D: Move Right
    Spacebar: Shoot
    Mouse: Aim  """
    start_time = 0
    time_alive = 0
    game_active = True
    wave_timer = 1
    wave_text = screen_height*.2
    start_time = 0
    pygame.time.set_timer((NEW_WAVE_EVENT), 1000, 1)
    #Loop to display first wave text before game begins
    while not pygame.event.peek(NEW_WAVE_EVENT): 
        draw_blinking_text("pokemon-gb-font\PokemonGb-RAeo.ttf",(screen_width/2, wave_text),"Wave 1", 100, .007, (700, 120))
        pygame.display.update()
    pygame.time.set_timer((ASTEROID_SPAWN), 750-int(math.log(wave_timer)*750))
    pygame.time.set_timer((NEW_WAVE_EVENT), 35000, 1)

    while True:
        wave_timer = int(get_time_alive(start_time, True)/35)+1#Every 35 seconds new wave will begin
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                bullet_group.add(Bullet(ship1.x, ship1.y, ship1.angle))
            if event.type == ASTEROID_SPAWN and game_active:
                asteroid_group.add(Asteroid(screen_height, screen_width, wave_timer, ship1.x, ship1.y))
            if event.type == NEW_WAVE_EVENT and game_active:
                pygame.event.set_blocked(ASTEROID_SPAWN)
                pygame.time.set_timer((ASTEROID_SPAWN), 750-int(math.log(wave_timer)*250))
                wave_text = screen_height*.2
            if event.type == BEGIN_NEW_WAVE and game_active:
                pygame.event.set_allowed(ASTEROID_SPAWN)
                pygame.time.set_timer((NEW_WAVE_EVENT), 35000, 1)

        if game_active:
            screen.fill((0,0,0))
            draw_blinking_text("pokemon-gb-font\PokemonGb-RAeo.ttf",(screen_width/2, 600),f"{get_time_alive(start_time, True)}", 100)
            time_alive = get_time_alive(start_time, True)
            if not asteroid_group and pygame.event.get_blocked(ASTEROID_SPAWN) and wave_text >-50:
                #Draws the next wave's number repeatedlty until it comes off screen and asteroids begin spawning 400 milisecnonds later
                draw_blinking_text("pokemon-gb-font\PokemonGb-RAeo.ttf",(screen_width/2, wave_text),f"Wave {wave_timer}", 100, .03)
                wave_text-= .8            
                pygame.time.set_timer(BEGIN_NEW_WAVE, 400, 1)
            if ship1.check_collision(asteroid_group):
                game_active = False
            #Key inputs
            if pressed[pygame.K_w]:
                ship1.move_forward()

            if pressed[pygame.K_a]:                     
                ship1.move_left()

            if pressed[pygame.K_s]:                                 
                ship1.move_backward()

            if pressed[pygame.K_d]:                               
                ship1.move_right()

            if pressed[pygame.K_0]:  
                time_alive = get_time_alive(start_time)                   
                game_active = False
            
            asteroid_group.update()
            asteroid_group.draw(screen)   
            bullet_group.update(asteroid_group)   
            bullet_group.draw(screen)
            ship_group.update()
            ship_group.draw(screen)
             
            
        else:
            #This condition displays the death screen and waits for input to either restart game or exit
            screen.fill((0,0,0))
            bullet_group.draw(screen)
            ship_group.draw(screen)
            asteroid_group.draw(screen)
            display_death_screen_text(time_alive)
            ship1.reset_values() 
            if pressed[pygame.K_SPACE]:
                start_time = int(pygame.time.get_ticks()/1000)
                bullet_group.empty()
                asteroid_group.empty()
                game_active = True
            elif pressed[pygame.K_ESCAPE]:
                pygame.quit
                exit()
        
                
        pygame.display.update()
        clock.tick(60)

#*********************End of Game Loop**************************

def get_time_alive(start_time: int, integer:bool = False ):
    """Returns the time alive in a string format as default. If int is true only the integer is returned"""
    time_alive = int((pygame.time.get_ticks()/1000)-start_time)
    if integer:
        return time_alive
    elif time_alive >= 60:
        time_alive = f"{int(time_alive/60)}".zfill(2)+":"+f"{time_alive%60}".zfill(2)
    return time_alive



def draw_blinking_text(font_type: str, coords:tuple, message:str, font_size: int, blink_interval = .01, blank_surface_size = (700, 100), font_color = (255,255,255)):
    """Draws blinking text using specfied coordinates, font_type, size, and message. Blink speed can be optionally altered. Every call of this function will stack speed of any other text called by this function. All functions called will be in sync"""
    global font_index
    off_text_surface = pygame.Surface(blank_surface_size)
    font = pygame.font.Font(font_type, font_size)
    font_text =[font.render(message, False, font_color), font.render(message, False, font_color), off_text_surface]
    font_rect = font_text[int(font_index)].get_rect(center =coords)
    screen.blit(font_text[int(font_index)], font_rect)
    font_index += blink_interval
    if font_index >= 2.8: #Resets the blink timer for the Retry and Game over message
        font_index = 0

def display_death_screen_text(time_alive):
    """Displays all relevant text and surfaces for the death screen. Also handles blinking for text"""
    #GAME OVER message
    draw_blinking_text("pokemon-gb-font\PokemonGb-RAeo.ttf",(screen_width/2,150 ),"GAME OVER", 50)
#    #Time_Alive message  
    draw_blinking_text("pokemon-gb-font\PokemonGb-RAeo.ttf",(screen_width/2,200 ),f"Time Alive: {time_alive}s", 25)
#    #Retry Key Message  
    draw_blinking_text("pokemon-gb-font\PokemonGb-RAeo.ttf",(screen_width/2,screen_height-200 ),"Press Space Bar to Retry", 25)
#     #Quit Messaage
    draw_blinking_text("pokemon-gb-font\PokemonGb-RAeo.ttf",(screen_width/2,screen_height-100 ),"Press ESC to Quit", 25)

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
    exit()