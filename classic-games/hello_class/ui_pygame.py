#!/usr/bin/env python

import os, sys
import classes
from ui import UserInterface
import pygame, sys, time
from pygame.locals import *

# This class defines the PyGame/SDL UI frontend

class SDLUserInterface(UserInterface):
    # Some constants

    # Colors
    CHR_COLOR_PLAYER = (0, 0, 0)
    CHR_COLOR_ENEMY = (255, 0, 0)
    CHR_COLOR_WIZARD = (0, 0, 255)
    CHR_COLOR_ARCHER = (255, 255, 255)
    CHR_COLOR_DEAD = (255, 255, 0)

    # Labels
    CHR_TXT_PLAYER = "S"
    CHR_TXT_ENEMY = "B"
    CHR_TXT_WIZARD = "W"
    CHR_TXT_ARCHER = "A"
    CHR_TXT_DEAD = "D"

    # Sizes
    STATUSBAR_HEIGHT=20
    CHR_SIZE=10

    # Directions
    DIRECTIONS = {
        K_RIGHT: "right",
        K_LEFT: "left",
        K_DOWN: "down",
        K_UP: "up"
    }


    def __init__(self, game_handler, width = 60, height = 22):
        super(SDLUserInterface, self).__init__(game_handler, width, height)

        statusbar_height = SDLUserInterface.STATUSBAR_HEIGHT
        map_width = width * SDLUserInterface.CHR_SIZE
        map_height = height * SDLUserInterface.CHR_SIZE

        # The main window must contain the map + the statusbar
        tot_height = statusbar_height + map_height
        tot_width = map_width

        pygame.init()
        pygame.display.set_caption('Hello Game')
        pygame.mouse.set_visible(0)

        basicFont = pygame.font.SysFont(None, 15)
        self.windowSurface = pygame.display.set_mode((tot_width, tot_height),
                0, 32)
        self.windowSurface.fill((255, 255, 255)) # white

        self.world_map = WorldMap(self.windowSurface,
                0, SDLUserInterface.STATUSBAR_HEIGHT, # X, Y
                width, height)

        self.statusbar = StatusBar(basicFont,
                self.windowSurface,
                self.world_map)

        #print """Welcome to 'Hello, Class' game
        #Available commands are:
        #r - move right
        #l - move left
        #u - move up
        #d - move down
        #a - attack
        #gps - print location
        #x - exit

        #There is a Bug 2 steps to the right from you.
        #You should probably do something about it!
        #"""
    
    def set_statusbar_character(self, character):
        self.statusbar.set_character(character)

    def draw_map(self):
        self.world_map.print_map()
        pygame.display.update()

    def get_student(self):
        return self.student

    def add_student(self, attributes):
        student = Player(self, attributes)
        self.student = student
        self.world_map.add_character(self.student)
        student.show()

    def add_engineer(self, attributes):
        wizard = Wizard(self, attributes)
        self.engineer = wizard
        self.world_map.add_character(self.engineer)
        wizard.show()

    def add_enemy(self, attributes):
        bug = Enemy(self, attributes)
        self.bugs.append(bug)
        self.world_map.add_character(bug)
        bug.show()

    def exit_loop(self):
        pygame.quit()
        sys.exit(0)

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                   self.exit_loop()
                elif event.type == KEYDOWN:
                    if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                        self.student.move(SDLUserInterface.DIRECTIONS[event.key])
                        for bug in self.bugs:
                            bug.act(self.student,
                                    SDLUserInterface.DIRECTIONS)
                        self.draw_map()
                    elif event.key == K_x:
                            self.exit_loop()
                    elif event.key == K_a:
                        for bug in self.bugs:
                            self.student.attack(bug)
                            bug.act(self.student,
                                    SDLUserInterface.DIRECTIONS)
                            self.draw_map()
            #c = raw_input("You > ")
            #elif c == "gps":
            #    self.statusbar.set_status("Your GPS location: %i %i" % (self.student.x, self.student.y))
            #    for bug in self.bugs:
            #        self.statusbar.set_status("Bug GPS location: %i %i" % (bug.x, bug.y))
            #elif c == "save":
            #    self.game_handler.save_game();
            #    self.statusbar.set_status("Game saved!")


# Canvas / Layout classes
class StatusBar(classes.StatusBar):
    def __init__(self, basicFont, windowSurface,
            world_map, character = None):
        super(StatusBar, self).__init__(character)
        self.basic_font = basicFont
        self.text = basicFont.render('Press "h" for help', True,
            (255, 255, 255), # White
            #(255, 0, 0), # Red
            (0, 0, 255) # Blue
            )
        self.world_map = world_map
        self.windowSurface = windowSurface
        self.show()

    def show(self):
        self.textRect = self.text.get_rect()
        self.textRect.topleft = (0, 0)
        self.windowSurface.blit(self.text, self.textRect)
        pygame.display.update()

    def set_character(self, character):
        pass # XXX
    #    self.character = character
    #    self.set_status()
    #    self.show()
        
    def set_status(self, msg = ''):
        self.text = self.basic_font.render(msg, True,
            (255, 255, 255), # White
            (0, 0, 255) # Blue
            )
        self.show()

class WorldMap(classes.WorldMap):
    def __init__(self, pos_x, pos_y, windowSurface, width, height):
        super(WorldMap, self).__init__(width, height)

    def print_map(self):
        for y in range(self.height - 1, 0, -1):
            for x in range(self.width):
                cell = self.map[x][y]
                if cell is not None:
                    cell.show()

    def add_character(self, character):
        self.map[character.x][character.y] = character

    def remove_character(self, character):
        self.map[character.x][character.y] = None

# Base Character class
class Character(classes.Character):

    def __init__(self, ui, attributes):
        pos_x = int(attributes[0])
        pos_y = int(attributes[1])
        hp = int(attributes[2])
        super(Character, self).__init__(ui, pos_x, pos_y, hp)
        self.windowSurface = ui.windowSurface
        self.rect = pygame.Rect(pos_x * SDLUserInterface.CHR_SIZE,
                    pos_y * SDLUserInterface.CHR_SIZE,
                    SDLUserInterface.CHR_SIZE,
                    SDLUserInterface.CHR_SIZE)
 
    def is_player(self):
        if self.text == SDLUserInterface.CHR_TXT_PLAYER:
            return True
        return False

    def set_dead(self):
        self.text = SDLUserInterface.CHR_TXT_DEAD
        self.color = SDLUserInterface.CHR_COLOR_DEAD
        self.hp = 0

    def show(self):
        pygame.draw.rect(self.windowSurface, self.color, self.rect)
        pygame.display.update()

    def get_label(self):
        return self.text

class Player(Character, classes.Player):
    def __init__(self, ui, attributes):
        Character.__init__(self, ui, attributes)
        self.text = SDLUserInterface.CHR_TXT_PLAYER
        self.color = SDLUserInterface.CHR_COLOR_PLAYER

class Enemy(Character, classes.Enemy):
    def __init__(self, ui, attributes):
        Character.__init__(self, ui, attributes)
        self.text = SDLUserInterface.CHR_TXT_ENEMY
        self.color = SDLUserInterface.CHR_COLOR_ENEMY

class Wizard(Character, classes.Wizard):
    def __init__(self, ui, attributes):
        Character.__init__(self, ui, attributes)
        self.text = SDLUserInterface.CHR_TXT_WIZARD
        self.color = SDLUserInterface.CHR_COLOR_WIZARD

class Archer(Character, classes.Archer):
    def __init__(self, ui, attributes):
        Character.__init__(self, ui, attributes)
        self.text = SDLUserInterface.CHR_TXT_ARCHER
        self.color = SDLUserInterface.CHR_COLOR_ARCHER

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
