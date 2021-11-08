import pygame
import os
import sys

pygame.font.init()  # text init
pygame.mixer.init()  # sound init

WIDTH, HEIGHT = 448, 576
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")

FPS = 60
VEL = 2
ENTITY_WIDTH, ENTITY_HEIGHT = 25, 25

MAP = pygame.image.load(os.path.join('Assets', 'map.png'))

RED_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'red-tmp.png')), (ENTITY_WIDTH, ENTITY_HEIGHT))
PAC_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'pac-tmp.png')), (ENTITY_WIDTH, ENTITY_HEIGHT))


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL


def handle_pac_movement(keys_pressed, pac):
    if keys_pressed[pygame.K_LEFT] and pac.x - VEL > 0:  # LEFT
        pac.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and pac.x + VEL + pac.width < WIDTH:  # RIGHT
        pac.x += VEL
    if keys_pressed[pygame.K_UP] and pac.y - VEL > 0:  # UP
        pac.y -= VEL
    if keys_pressed[pygame.K_DOWN] and pac.y + VEL + pac.height < HEIGHT:  # DOWN
        pac.y += VEL


def draw_window(red, pac):
    WIN.fill((0, 0, 0))
    WIN.blit(MAP, (0, 0))
    WIN.blit(RED_IMAGE, (red.x, red.y))
    WIN.blit(PAC_IMAGE, (pac.x, pac.y))

    pygame.display.update()


def main():
    # rettangoli per le hitbox dei personaggi
    red = pygame.Rect(WIDTH//2, HEIGHT//2, ENTITY_WIDTH, ENTITY_HEIGHT)
    pac = pygame.Rect(WIDTH//2, HEIGHT//2, ENTITY_WIDTH, ENTITY_HEIGHT)

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        handle_red_movement(keys_pressed, red)
        handle_pac_movement(keys_pressed, pac)

        draw_window(red, pac)

    main()  # per riavviare il gioco quando finisce, per ora è inutile


if __name__ == "__main__":
    main()
