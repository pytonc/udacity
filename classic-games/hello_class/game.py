#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
import getopt, sys
import ConfigParser
from hello_game import HelloGame

import time

def print_help():
    print sys.argv[0] + ' -h|--help -g|--gui=sdl'
    print 'gui accept the following values:'
    print 'sdl\t will use the pygame/SDL frontend'
    print 'txt\t will use the embedded ASCII frontend'

if __name__ == '__main__':
    # Initialize some defaults, before the cmdline parsing
    # XXX guy_backend = "sdl"
    config_file = "game.ini"
    config = ConfigParser.ConfigParser()
    frontend = None

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
            frontend = arg
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

    if frontend != None:
        game = HelloGame(config, frontend = frontend)
    else:
        game = HelloGame(config)

    game.start_game("Level1");
    sys.exit(0)

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
