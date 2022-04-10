import sys

import pygame
from pygame.locals import *
import os

# Game Initialization
pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
WIDTH = 800
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Game Fonts
PathMenuFont = 'Fonts/Retro.ttf'

# Game Framerate
clock = pygame.time.Clock()
FPS = 30

# background
background = pygame.image.load('Icons/mainmenuBackground.jpg').convert_alpha()


# Main Menu
def main_menu():
    menu = True
    selected = "start"
    os.system('start cmd /C python Player.py')
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        pygame.quit()
                        os.system('python firstGame.py')
                        quit()
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(blue)
        title = text_format("Space invasion", PathMenuFont, 90, yellow)
        if selected == "start":
            text_start = text_format("START", PathMenuFont, 75, green)
        else:
            text_start = text_format("START", PathMenuFont, 75, white)
        if selected == "quit":
            text_quit = text_format("QUIT", PathMenuFont, 75, green)
        else:
            text_quit = text_format("QUIT", PathMenuFont, 75, white)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(background, (0, 0))
        screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(FPS)


# Initialize the Game
main_menu()
pygame.quit()
quit()
