#!/usr/bin/env python
# hello_game.py
# This file implements the main class that will control a Gameplay

from classes import *
from ui_pygame import *
from ui_txt import *
import pickle


# This class implements what we could call a game handler
# It's responsible for parsing the configuration, setting up
# the characters and the UI and handling the end of the game
class HelloGame(object):
    def __init__(self, config, frontend="sdl"):
        self.config = config

        map_width = config.getint("WordMap", "width")
        map_height = config.getint("WordMap", "height")

        self.avail_levels = config.get("Levels", "available_levels")

        # Initialize game Frontend
        if frontend == "sdl":
            print "Initializing PyGame / SDL frontend"
            if map_width > 0 and map_height > 0:
                self.ui = SDLUserInterface(self, map_width, map_height)
            else:
                self.ui = SDLUserInterface(self)
        elif frontend == "txt":
            print "Initializing ASCII frontend"
            if map_width > 0 and map_height > 0:
                self.ui = TXTUserInterface(self, map_width, map_height)
            else:
                self.ui = TXTUserInterface(self)
        else:
            print "Unknown UI frontend " + frontend + ". Aborting!"
            sys.exit(2)

        savefile = config.get("GameHandler", "savefile")
        if savefile is not None:
            self.savefile = savefile

    # This loop controls the level progression
    def start_game(self):
        next_level = 1
        while True:
            self.start_level(next_level)
            next_level = self.get_next_level()

            if self.is_game_over():
                print "Game is OVER!"
                self.game_over(False)
            if next_level < 0:
                print "No more levels!"
                self.game_over(True)

            print "Loading level " + str(next_level)
            # Reset the UI "entities" before loading the next level
            self.ui.notify_level_finished()
            self.ui.reset()

    def start_level(self, level=1):
        level_label = "Level" + str(level)

        student_data = self.config.get(level_label, 'student').split(',')
        self.ui.add_student(student_data)
        self.curr_level = level

        engineer_data = self.config.get(level_label, 'engineer').split(',')
        self.ui.add_engineer(engineer_data)

        bugs_data = self.config.get(level_label, 'bug').split(';')
        for el in bugs_data:
            self.ui.add_enemy(el.split(','))

        self.ui.set_statusbar_character(self.ui.get_student())
        self.ui.set_status("Started level " + str(self.curr_level))

        self.ui.draw_window()
        self.ui.mainloop()

    def is_game_over(self):
        student = self.ui.get_student()
        if student.hp <= 0:
            print "You died!!"
            return True
        else:
            return False

    def is_level_finished(self):
        enemies = self.ui.get_enemies()
        for enemy in enemies:
            if enemy.hp > 0:
                return False
        return True

    def get_next_level(self):
        next_level = self.curr_level + 1
        level_label = "Level" + str(next_level)

        if level_label in self.avail_levels:
            return next_level
        else:
            return -1

    def game_over(self, victory):
        if victory == True:
            self.ui.notify_level_finished()
        else:
            self.ui.notify_game_over()
        self.quit_game()

    def quit_game(self):
        print "Exiting the game !"
        sys.exit(0)

    def save_game(self):
        outfile = open(self.savefile, "wb")
        pickle.dump(self.ui, outfile)
        outfile.close()

    def load_saved_game(self):
        pass

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
