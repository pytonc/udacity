#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
from classes import *

if __name__ == '__main__':
    #initializing some entities

    #campus = World(100, 100)

    student = Character(10, 10, 'S', 100)
    engineer = Wizard(20, 10, 100)
    bug1 = Enemy(12, 10, 100)
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

    world.print_map()

    while True:
        c = raw_input("You > ")
        if c == "x":
            break
        elif c == "r":
            student.move("right")
            #print "You now are at location: ", student.x, student.y
            world.print_map()
        elif c =="l":
            student.move("left")
            #print "You now are at location: ", student.x, student.y
            world.print_map()
        elif c =="u":
            student.move("up")
            #print "You now are at location: ", student.x, student.y
            world.print_map()
        elif c =="d":
            student.move("down")
            #print "You now are at location: ", student.x, student.y
            world.print_map()
        elif c == "gps":
            print "Your GPS location: ", student.x, student.y
            print "Bug GPS location: ", bug1.x, bug1.y
        elif c == "a":
            student.attack(bug1)
            print "Bug now has: ", bug1.hp, " hp left"
            world.print_map()
        else:
            print "Unknown command. 'x' to exit the game"


