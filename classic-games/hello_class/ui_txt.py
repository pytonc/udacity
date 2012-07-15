#!/usr/bin/env python

import os, sys
import classes
from ui import UserInterface

# This class defines the ASCII UI frontend

class TXTUserInterface(UserInterface):
    CHR_PLAYER = "S"
    CHR_ENEMY = "B"
    CHR_WIZARD = "W"
    CHR_ARCHER = "A"
    CHR_DEAD = "X"

    def __init__(self, game_handler, width = 60, height = 22):
        super(TXTUserInterface, self).__init__(game_handler, width, height)
        self.world_map = WorldMap(width, height)
        self.statusbar = StatusBar(self.world_map)

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
    
    def set_statusbar_character(self, character):
        self.statusbar.set_character(character)

    def draw_map(self):
        self.world_map.print_map()
        self.statusbar.show()

    def get_student(self):
        return self.student

    def add_student(self, attributes):
        student = Player(self, attributes)
        self.student = student
        self.world_map.add_character(self.student)

    def add_engineer(self, attributes):
        wizard = Wizard(self, attributes)
        self.engineer = wizard
        self.world_map.add_character(self.engineer)

    def add_enemy(self, attributes):
        bug = Enemy(self, attributes)
        self.bugs.append(bug)
        self.world_map.add_character(bug)

    def mainloop(self):
        while True:
            c = raw_input("You > ")
            
            if c == "x":
                break
            elif c in UserInterface.DIRECTIONS:
                self.student.move(UserInterface.DIRECTIONS[c])
                for bug in self.bugs:
                    bug.act(self.student, UserInterface.DIRECTIONS)
            elif c == "gps":
                self.statusbar.set_status("Your GPS location: %i %i" % (self.student.x, self.student.y))
                for bug in self.bugs:
                    self.statusbar.set_status("Bug GPS location: %i %i" % (bug.x, bug.y))
            elif c == "a":
                for bug in self.bugs:
                    self.student.attack(bug)
                    bug.act(self.student, UserInterface.DIRECTIONS)
            elif c == "save":
                self.game_handler.save_game();
                self.statusbar.set_status("Game saved!")
            elif c == "load":
                self.game_handler.load_saved_game();
                self.statusbar.set_status("Game reloaded!")
            else:
                self.statusbar.set_status("Unknown command. 'x' to exit game")
                
            self.draw_map()


# Canvas / Layout classes
class StatusBar(classes.StatusBar):
    def __init__(self, world_map, character = None):
        super(StatusBar, self).__init__(character)
        self.world_map = world_map

    def format_line(self, txt, width):
        line = "+ %s" % txt
        line += " " * (width - (len(line))) + " +"
        return line

    def show(self):
        self.set_status()
        print "+" * (self.world_map.width + 2)
        print self.format_line(self.line1, self.world_map.width)
        print self.format_line(self.line2, self.world_map.width)
        self.msg = ''

    def set_character(self, character):
        self.character = character
        self.set_status()
        self.show()
        
    def set_status(self, msg = ''):
        self.msg = (msg, '::'.join((self.msg, msg)))[len(self.msg) > 0]
        status = "HP: %i/%i" % (self.character.hp, self.character.max_hp)
        msgs = self.msg.split('::')
        
        self.line1 = "%s + %s" % (status, msgs[0])
        if len(msgs) > 1:
            self.line2 = "%s + %s" % (' ' * len(status), msgs[1])
        else:
            self.line2 = "%s + %s" % (' ' * len(status), ' ' * len(msgs[0]))

class WorldMap(classes.WorldMap):
    def __init__(self, width, height):
        super(WorldMap, self).__init__(width, height)

    def print_map(self):
        print '+' * (self.width + 2)
        for y in range(self.height - 1, 0, -1):
            line = '+'
            for x in range(self.width):
                cell = self.map[x][y]
                if cell is None:
                    line += ' '
                else:
                    line += cell.image
            print line + '+'
        print '+' * (self.width + 2)

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

    def is_player(self):
        if self.image == TXTUserInterface.CHR_PLAYER:
            return True
        return False

    def set_dead(self):
        self.image = TXTUserInterface.CHR_DEAD
        self.hp = 0

    def get_label(self):
        return self.image

class Player(Character, classes.Player):
    def __init__(self, ui, attributes):
        Character.__init__(self, ui, attributes)
        self.image = TXTUserInterface.CHR_PLAYER

class Enemy(Character, classes.Enemy):
    def __init__(self, ui, attributes):
        Character.__init__(self, ui, attributes)
        self.image = TXTUserInterface.CHR_ENEMY

class Wizard(Character, classes.Wizard):
    def __init__(self, ui, attributes):
        Character.__init__(self, ui, attributes)
        self.image = TXTUserInterface.CHR_WIZARD

class Archer(Character, classes.Archer):
    def __init__(self, ui, attributes):
        Character.__init__(self, ui, attributes)
        self.image = TXTUserInterface.CHR_ARCHER

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
