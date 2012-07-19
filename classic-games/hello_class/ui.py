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

    def get_student(self):
        return self.student

    def get_enemies(self):
        return self.bugs

    def reset(self):       
        self.world_map.reset()
        self.bugs = []
        self.engineer = None
        self.student = None

    # This function must be called at every loop iteration
    # It'll check for level completed / game over conditions
    def exit_loop(self):
        if self.game_handler.is_game_over() == True or self.game_handler.is_level_finished() == True:
            return True
        return False

    def notify_level_finished(self):
        pass

    def notify_game_over(self):
        pass

class StatusBar(object):
    def __init__(self, character=None):
        self.character = character
        self.msg = ''

    def set_msg(msg=''):
        self.msg = msg

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
