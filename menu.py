import pygame
import sys
from pygame.locals import *
import game
import agent
import os

mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((game.WIDTH, game.HEIGHT), 0, 32)

font = pygame.font.Font(os.path.join('Assets', 'emulogic.ttf'),10)
pacfont = pygame.font.Font(os.path.join('Assets', 'CrackMan.ttf'),30) #scegli tra questo e PAC-FONT

menu_image = pygame.image.load(os.path.join('Assets', 'Final_menu.png'))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    click = False
    print(pygame.font.get_fonts())

    while True:

        screen.fill((0, 0, 0))
        screen.blit(menu_image, (2, 2))
        imagerect = menu_image.get_rect()
        draw_text('ThE PhAnToM MeNaCe', pacfont, (255, 255, 255), screen, (game.WIDTH/2), imagerect.height+10)
        draw_text('Press Esc to exit anytime', font, (255, 255, 255), screen, (game.WIDTH / 2), imagerect.height + 50)



        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(1, 1, 200, 50)
        button_1.center = ((game.WIDTH/2), (game.HEIGHT/2)+50)
        button_2 = pygame.Rect(1, 1, 200, 50)
        button_2.center = ((game.WIDTH / 2), (game.HEIGHT / 2) + 150)
        if button_1.collidepoint((mx, my)):
            if click:
                play()
        if button_2.collidepoint((mx, my)):
            if click:
                auto()
        pygame.draw.rect(screen, (230, 220, 22), button_1)
        pygame.draw.rect(screen, (230, 220, 22), button_2)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def play():
    game.main()


def auto():
    agent.play()


if __name__ == "__main__":
    main_menu()
