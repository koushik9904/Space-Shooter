import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH,HEIGHT)


SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40


BORDER_WIDTH = 10
BORDER_HEIGHT = HEIGHT


VELOCITY = 5
PROJECTILE_VELOCITY = 10
PROJECTILE_WIDTH = 15
PROJECTILE_HEIGHT = 5
MAX_BULLETS = 3


FONT = pygame.font.SysFont("aerial",36)
WIN_FONT = pygame.font.SysFont("aerial",72)


RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2


RED_HEALTH = 10
YELLOW_HEALTH = 10


SPACESHIP_SIZE = (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
BORDER = pygame.Rect(WIDTH/2-BORDER_WIDTH/2,0,BORDER_WIDTH,BORDER_HEIGHT)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BULLET_HIT_SOUND = pygame.mixer.Sound("assets/Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("assets/Gun+Silencer.mp3")

YELLOW_SPACESHIP_IMAGE = pygame.image.load("assets/spaceship_yellow.png")
RED_SPACESHIP_IMAGE = pygame.image.load("assets/spaceship_red.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,SPACESHIP_SIZE),90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,SPACESHIP_SIZE),270)

SPACE = pygame.transform.scale(pygame.image.load("assets/space.png"),SIZE)
WINDOW = pygame.display.set_mode(SIZE)
pygame.display.set_caption("warships")

def fire(x,y):
    projectile = pygame.Rect(x,y,PROJECTILE_WIDTH,PROJECTILE_HEIGHT)

def draw(red,yellow,red_bullets,yellow_bullets):
    WINDOW.fill(WHITE)
    WINDOW.blit(SPACE,(0,0))
    pygame.draw.rect(WINDOW,BLACK,BORDER)
    WINDOW.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WINDOW.blit(RED_SPACESHIP,(red.x,red.y))
    Helath_text = FONT.render(f"HEALTH:{round(YELLOW_HEALTH)}",1,YELLOW)
    Helath_text2 = FONT.render(f"HEALTH:{round(RED_HEALTH)}",1,RED)
    # win_text = FONT.render(f"")
    WINDOW.blit(Helath_text,(10,10))
    WINDOW.blit(Helath_text2,(WIDTH-Helath_text2.get_width()-5,10))

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW,YELLOW,bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW,RED,bullet)

    pygame.display.update()
    
def move_yellow(keys,yellow): 
    if keys[pygame.K_w] == True and yellow.y - VELOCITY > 0:
        yellow.y -= VELOCITY
    elif keys[pygame.K_a] == True and yellow.x - VELOCITY > 0:
        yellow.x -= VELOCITY
    elif keys[pygame.K_d] == True and yellow.x + VELOCITY + yellow.width - 15 < BORDER.x:
        yellow.x += VELOCITY
    elif keys[pygame.K_s] == True and yellow.y + VELOCITY + SPACESHIP_HEIGHT + 10 < HEIGHT:
        yellow.y += VELOCITY

def move_red(keys,red):  
    if keys[pygame.K_UP] == True and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    elif keys[pygame.K_LEFT] == True and red.x - VELOCITY > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    elif keys[pygame.K_RIGHT] == True and red.x + VELOCITY + red.width < WIDTH:
        red.x += VELOCITY
    elif keys[pygame.K_DOWN] == True and red.y + VELOCITY + SPACESHIP_HEIGHT + 10 < HEIGHT:
        red.y += VELOCITY
    

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    global YELLOW_HEALTH
    global RED_HEALTH
    for bullet in yellow_bullets:
        bullet.x += PROJECTILE_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            RED_HEALTH -= 1
            yellow_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        if bullet.x + bullet.width >= WIDTH:
            yellow_bullets.remove(bullet)
        
    for bullet in red_bullets:
        bullet.x -= PROJECTILE_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            YELLOW_HEALTH -= 1
            red_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        if bullet.x <= 0:
            red_bullets.remove(bullet)





def main():
    run = True
    clock = pygame.time.Clock()
    yellow = pygame.Rect(200,HEIGHT/2-SPACESHIP_HEIGHT/2,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red = pygame.Rect(WIDTH-200,HEIGHT/2-SPACESHIP_HEIGHT/2,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []
    while run:
        clock.tick(60)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False
                break
            
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height/2,PROJECTILE_WIDTH,PROJECTILE_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    # handle_bullets(yellow_bullets,red_bullets,yellow,red)
                if events.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x,red.y+red.height/2,PROJECTILE_WIDTH,PROJECTILE_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
        
        keys = pygame.key.get_pressed()
        move_red(keys,red)
        move_yellow(keys,yellow)
        
        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        if YELLOW_HEALTH <= 0:
            win_text = WIN_FONT.render(f"RED WINS!!!",1,RED)
            WINDOW.blit(win_text,(WIDTH/2 - win_text.get_width()/2,HEIGHT/2 - win_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            run = False
            break

        if RED_HEALTH <= 0:
            win_text = WIN_FONT.render(f"YELLOW WINS!!!",1,YELLOW)
            WINDOW.blit(win_text,(WIDTH/2 - win_text.get_width()/2,HEIGHT/2 - win_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            run = False
            break

        draw(red,yellow,red_bullets,yellow_bullets)

    pygame.quit()



if __name__ == "__main__":
    main()