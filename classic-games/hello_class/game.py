#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects

# Hacked by MikeGoldberg to use Pygame
# Mon Jul 16 12:51:31 CDT 2012

from classes import *
import pygame
from pygame.locals import *
import os

DIRECTIONS = {
    "r": "right",
    "l": "left",
    "d": "down",
    "u": "up"
}

# Pygame (SDL) constants
XRES = 640
YRES = 480
BCOLOR = (255, 255, 255)
BLOCK_SIZE=10 # must match value in other file! This has to be bad.

# Pygame: update the graphical screen
def update_screen(players, screen):
    screen.blit(background, (0, 0))
    for player in players:
        player.screen.blit(player.sprite, (10*player.x, (22*21 - 22*player.y)))
    pygame.display.flip()

if __name__ == '__main__':

    print """Welcome to 'Hello, Class' game
    Available commands are:
    r - move right
    l - move left
    u - move up
    d - move down
    a - attack
    gps - print location
    x - exit

    There is a Bug 2 steps to the right from you.
    You should probably do something about it!
    """

    # initializing some entities
    players = []

    # Pygame: set up
    pygame.display.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
    screen = pygame.display.set_mode((XRES, YRES))
    pygame.display.set_caption('Udacity CS101 Game')
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()

    # Pygame: Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BCOLOR)

    #Pygame: Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #campus = World(100, 100)
    student = Player(10, 10, screen, 100)
    players.append(student)
    engineer = Wizard(35, 14, screen, 100)
    players.append(engineer)
    bug1 = Enemy(12, 10, screen, 100)
    players.append(bug1)

    pygame.display.flip()

    statusbar.set_character(student)
    #world.print_map()

    c = ''
    while True:
        #c = raw_input("You > ")

        #if c == "x":
        #    break
        #elif c in DIRECTIONS:
        #    student.move(DIRECTIONS[c])
        #    bug1.act(student, DIRECTIONS)
        #    update_screen(players, screen)
        #elif c == "gps":
        #    statusbar.set_status("Your GPS location: %i %i" % (student.x, student.y))
        #    statusbar.set_status("Bug GPS location: %i %i" % (bug1.x, bug1.y))
        #elif c == "a":
        #    student.attack(bug1)
        #    bug1.act(student, DIRECTIONS)
        #else:
        #    pass
        #    #statusbar.set_status("Unknown command. 'x' to exit game")
        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.display.quit()
            elif event.type == KEYDOWN and event.key == K_r or \
                 event.type == KEYDOWN and event.key == K_RIGHT:
                c = 'r'
                student.move(DIRECTIONS[c])
                bug1.act(student, DIRECTIONS)
            elif event.type == KEYDOWN and event.key == K_l or \
                 event.type == KEYDOWN and event.key == K_LEFT:
                c = 'l'
                student.move(DIRECTIONS[c])
                bug1.act(student, DIRECTIONS)
            elif event.type == KEYDOWN and event.key == K_u or \
                 event.type == KEYDOWN and event.key == K_UP:
                c = 'u'
                student.move(DIRECTIONS[c])
                bug1.act(student, DIRECTIONS)
            elif event.type == KEYDOWN and event.key == K_d or \
                 event.type == KEYDOWN and event.key == K_DOWN:
                c = 'd'
                student.move(DIRECTIONS[c])
                bug1.act(student, DIRECTIONS)
            elif event.type == KEYDOWN and event.key == K_x:
                pygame.display.quit()
            update_screen(players, screen)

        #statusbar.show()
        #world.print_map()


