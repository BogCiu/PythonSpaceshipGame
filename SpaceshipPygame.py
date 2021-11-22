import pygame
import os

width = 400
height = 400
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("First game!")
VEL = 5
BULLET_VEL = 10

BACKGROUND = (160, 160, 160)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(width // 2 - 5, 0, 10, height)
FPS = 60
SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(RED_SPACESHIP_IMAGE, -90)


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VEL < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < height - 10:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x + BORDER.width:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + yellow.width + VEL < width:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + yellow.height + VEL < height - 10:  # DOWN
        yellow.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > width - 4:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.fill(BACKGROUND)
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def main():
    red = pygame.Rect(325, 180, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(25, 180, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    max_bullets = 3
    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.WINDOWMINIMIZED:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 8, 4)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 8, 4)
                    red_bullets.append(bullet)

        print(f'{yellow_bullets}___________{red_bullets}')
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets)

    pygame.quit()


if __name__ == "__main__":
    main()

# https://youtu.be/jO6qQDNa2UY?t=4421
