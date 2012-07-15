#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
from classes import *
from ui_pygame import *
from ui_txt import *
import getopt, sys
import ConfigParser

import time

def print_help():
    print sys.argv[0] + ' -h|--help -g|--gui=sdl'
    print 'gui accept the following values:'
    print 'sdl\t will use the pygame/SDL frontend'
    print 'txt\t will use the embedded ASCII frontend'

if __name__ == '__main__':
    # Initialize some defaults, before the cmdline parsing
    # XXX guy_backend = "sdl"
    guy_backend = "txt"
    config_file = "game.ini"
    config = ConfigParser.ConfigParser()

    # Read command line parameter
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                "hg:c:",
                ["help", "gui=", "config="])
    except getopt.GetoptError:
        print_help()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            sys.exit()
        elif opt in ("-g", "--gui"):
            guy_backend = arg
        elif opt in ("-c", "--config"):
            config_file = arg
        else:
            print "Unknown option: " + opt
            print_help()
            sys.exit(1)

    # Read the config file
    try:
        config.read(config_file)
    except:
       print "Error reading config file " + config_file
       sys.exit(3)

    map_width = config.getint("WordMap", "width")
    map_height = config.getint("WordMap", "height")

    # Initialize game Frontend
    if guy_backend == "sdl":
        print "Initializing PyGame / SDL frontend"
        if map_width > 0 and map_height > 0:
            ui = SDLUserInterface(maps_width, map_height)
        else:
            ui = SDLUserInterface()
    elif guy_backend == "txt":
        print "Initializing ASCII frontend"
        if map_width > 0 and map_height > 0:
            ui = TXTUserInterface(map_width, map_height)
        else:
            ui = TXTUserInterface()
    else:
        print "Unknown UI frontend " + guy_backend + ". Aborting!"
        sys.exit(2)

    # Set up the current level
    level = "Level1"

    student_data = config.get(level, 'student').split(',')
    ui.add_student(student_data)

    engineer_data = config.get(level, 'engineer').split(',')
    ui.add_engineer(engineer_data)

    bugs_data = config.get(level, 'bug').split(';')
    for el in bugs_data:
        ui.add_enemy(el.split(','))

    ui.set_statusbar_character(ui.get_student())

    ui.draw_map()
    ui.mainloop()

    sys.exit(0)

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
