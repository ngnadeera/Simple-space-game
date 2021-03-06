
import pygame
import os
pygame.font.init()
pygame.mixer.init()


WIDTH , HEIGHT = 900,500  #WIDTH AND THE HIGHT OF THE GAME
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("First Game") #set the name of the game
BORDER = pygame.Rect(WIDTH//2 -5,0,10,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3', )
BULLET_FAIRE_SOUND =pygame.mixer.Sound('Assets/Gun+Silencer.mp3', )


HEALTH_FONT = pygame.font.SysFont('comicsans', 40 )
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)


VEL = 10
BULLETS_VEL = 8
MAX_BULLET = 10
FPS = 60 #how frames per second we wanted our game to update


SPACESHIP_WIDTH , SPACESHIP_HEIGHT = 55 , 40

YELLOW_HIT = pygame.USEREVENT + 1   # defines the first user event
RED_HIT = pygame.USEREVENT + 2     # defines the second user event

YELLOW_SPACESHIP_IMAGE  = pygame.image.load(os.path.join(
    'Assets','spaceship_yellow.png')) #surfaces
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90) #downsize the scale
pygame.transform.rotate(YELLOW_SPACESHIP, 90)
RED_SPACESHIP_IMAGE  = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))  #surfaces
RED_SPACESHIP =pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')) , (WIDTH,HEIGHT))


def draw_window(yellow,red,red_bullets,yellow_bullets,red_health,yellow_health):
    
         WIN.blit(SPACE , (0,0))
         red_health_text = HEALTH_FONT.render("Health:" + str(red_health),1,WHITE)
         yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health),1,WHITE)
         
         WIN.blit(red_health_text,(WIDTH - red_health_text.get_width()-10,10))
         WIN.blit(yellow_health_text,(10,10))

         
         WIN.blit(YELLOW_SPACESHIP , (yellow.x,yellow.y))  #cordinates from the top bottom
         WIN.blit(RED_SPACESHIP,(red.x,red.y))
         pygame.draw.rect(WIN, BLACK, BORDER)
         
         for bullet in red_bullets:
             pygame.draw.rect(WIN, RED, bullet)
             
         for bullet in yellow_bullets:
             pygame.draw.rect(WIN, YELLOW, bullet)
         
         pygame.display.update() #to see resent changes we have to manually update the display

def yellow_movement(keys_pressed,yellow):
    
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_d] and yellow.x - VEL + yellow.width < BORDER.x: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y - VEL+ 30 + yellow.height < 500: #down 
        yellow.y += VEL
        
def red_movement(keys_pressed,red):
    
    if keys_pressed[pygame.K_LEFT] and red.x - VEL  > BORDER.x + BORDER.width : #left 
        red.x -= VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x - VEL + red.width < WIDTH: #right
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y - VEL+ 30 + red.height < 500: #down
        red.y += VEL
        
def handel_bullets (yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            BULLET_HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            
        elif bullet.x  > WIDTH:
            yellow_bullets.remove(bullet)
     
    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet): #if yellow spaceship colider with the bullet this will create a event and remove the bullet from the list
            BULLET_HIT_SOUND.play()

            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            
        elif bullet.x < 0:
            red_bullets.remove(bullet)
            
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH //2 - draw_text.get_width()//2,HEIGHT//2 - draw_text.get_height()//2 ))
    pygame.display.update()
    pygame.time.delay(5000)
            
def main():
    
    red_bullets = []
    yellow_bullets = []
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT) #(X position,Y position,width,height)
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    run = True
    
    red_health = 10
    yellow_health = 10
    
    while run:
         clock.tick(FPS)
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height //2 -2 , 10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FAIRE_SOUND.play()
                    
                    
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(
                        red.x , red.y + red.height //2 -2 , 10,5)
                    red_bullets.append(bullet)
                    BULLET_FAIRE_SOUND.play()

                    
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_FAIRE_SOUND.play()

                
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_FAIRE_SOUND.play()
                
                   
         winner_text = ""
         if red_health < 0:
             winner_text = "Yellow Wins !"
             
         if yellow_health < 0 :
             winner_text = "Red Wins !"
         if winner_text != "":
             draw_winner(winner_text)
             break
          
         keys_pressed = pygame.key.get_pressed()
         yellow_movement(keys_pressed, yellow)
         red_movement(keys_pressed, red)
          
             
         handel_bullets (yellow_bullets,red_bullets,yellow,red)
         draw_window(yellow, red,red_bullets,yellow_bullets,red_health,yellow_health)         
    main()

if __name__ == "__main__":

    main()
        
    