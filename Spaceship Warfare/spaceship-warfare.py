import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Warfare!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets/Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets/Gun+Silencer.mp3'))

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACE_IMAGE = pygame.image.load(os.path.join('Assets/space.png'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets/spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)) # resizing yellow_spaceship
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90) # rotate the yellow_spaceship 90 degrees
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets/spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)) # resizing red_spaceship 
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270) # rotate the red_spaceship 270 degrees 

def draw_window(yellow_player, red_player, yellow_bullets, red_bullets, yellow_health, red_health):
        # WINDOW.fill(WHITE)
        WINDOW.blit(SPACE, (0, 0))
        pygame.draw.rect(WINDOW, BLACK, BORDER)

        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
        WINDOW.blit(yellow_health_text, (10, 10))
        WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

        WINDOW.blit(YELLOW_SPACESHIP, (yellow_player.x, yellow_player.y)) # image, (position x & y)
        WINDOW.blit(RED_SPACESHIP, (red_player.x, red_player.y)) # image, (position x & y)
        
        for bullet in yellow_bullets:
            pygame.draw.rect(WINDOW, YELLOW, bullet)

        for bullet in red_bullets:
            pygame.draw.rect(WINDOW, RED, bullet)
        
        pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow_player):
    if keys_pressed[pygame.K_a] and yellow_player.x - VELOCITY > 0: # LEFT KEY 'A'
        yellow_player.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow_player.x + VELOCITY + yellow_player.width < BORDER.x: # RIGHT KEY 'D'
        yellow_player.x += VELOCITY 
    if keys_pressed[pygame.K_w] and yellow_player.y  - VELOCITY > 0: # UP KEY 'W'
        yellow_player.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow_player.y + VELOCITY + yellow_player.height < HEIGHT - 15: # DOWN KEY 'S'
        yellow_player.y += VELOCITY 

def red_handle_movement(keys_pressed, red_player):
    if keys_pressed[pygame.K_LEFT] and red_player.x - VELOCITY > BORDER.width + BORDER.x + 15: # LEFT KEY '<-'
        red_player.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red_player.x + VELOCITY + red_player.width < WIDTH + 15: # RIGHT KEY '->'
        red_player.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red_player.y - VELOCITY > 0: # UP KEY 'PgUp'
        red_player.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red_player.y + VELOCITY + red_player.height < HEIGHT - 15: # DOWN KEY 'PgDn'
        red_player.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow_player, red_player):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text, color):
    draw_text = WINNER_FONT.render(text, 1, color)
    WINDOW.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    
    pygame.display.update()
    pygame.time.delay(5000)

def main():

    YELLOW_PLAYER = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # (x, y, wifth, height)
    RED_PLAYER = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # (x, y, width, height)

    YELLOW_BULLETS = []
    RED_BULLETS = []

    YELLOW_HEALTH = 10
    RED_HEALTH = 10

    clock = pygame.time.Clock()

    run = True 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(YELLOW_BULLETS) < MAX_BULLETS:
                    bullet = pygame.Rect(YELLOW_PLAYER.x + YELLOW_PLAYER.width, YELLOW_PLAYER.y + YELLOW_PLAYER.height // 2 - 2, 10, 5)
                    YELLOW_BULLETS.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(RED_BULLETS) < MAX_BULLETS:
                    bullet = pygame.Rect(RED_PLAYER.x, RED_PLAYER.y + RED_PLAYER.height // 2 - 2, 10, 5)
                    RED_BULLETS.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RED_HIT:
                RED_HEALTH -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        winner_color = WHITE
        if YELLOW_HEALTH <= 0:
            winner_text = "RED WINS !!!"
            winner_color = RED
        if RED_HEALTH <= 0:
            winner_text = "YELLOW WINS !!!"
            winner_color = YELLOW
        if winner_text != "":
            draw_winner(winner_text, winner_color)
            break

        KEY_PRESSED = pygame.key.get_pressed() # what keys are currently being pressed 
        yellow_handle_movement(KEY_PRESSED, YELLOW_PLAYER)
        red_handle_movement(KEY_PRESSED, RED_PLAYER)

        handle_bullets(YELLOW_BULLETS, RED_BULLETS, YELLOW_PLAYER, RED_PLAYER)
        
        draw_window(YELLOW_PLAYER, RED_PLAYER, YELLOW_BULLETS, RED_BULLETS, YELLOW_HEALTH, RED_HEALTH)

    # pygame.quit()
    main()

if __name__ == "__main__":
    main()