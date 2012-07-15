#!/usr/bin/env python
import classes

# This class defines an interface for any UI frontend
class UserInterface(object):
    DIRECTIONS = {
        "r": "right",
        "l": "left",
        "d": "down",
        "u": "up"
    }

    def __init__(self, game_handler, width, height):
        self.game_handler = game_handler
        self.student = None
        self.engineer = None
        self.bugs = []
        self.statusbar = None

    def add_student(self, args):
        self.student = classes.Player(*args)

    def add_engineer(self, args):
        self.engineer = classes.Wizard(*args)

    def add_enemy(self, args):
        bug = classes.Enemy(*args)
        self.bugs.append(bug)

    def set_statusbar_character(self, character):
        self.statusbar.set_character(character)

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
