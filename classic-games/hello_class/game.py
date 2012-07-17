#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
from classes import *
        
DIRECTIONS = {
    "r": "right",
    "l": "left",
    "d": "down",
    "u": "up"
}

if __name__ == '__main__':

    print """Welcome to 'Hello, Class' game
    Available commands are:
    r - move right
    l - move left
    u - move up
    d - move down
    a - attack
    i - show list of items
    p ([n]) - pick something up or pick an item [n] from a chest
    drop [n] - put an item [n] in a chest or drop it
    draw [n] - draw weapon with position [n] in inventory
    gps - print location
    x - exit
    
    There is a Bug 2 steps to the right from you.
    In the chest to your left might be something that helps.
    You should probably do something about it!
    """

    # initializing some entities

    #campus = World(100, 100)
    student = Player(10, 10, 100)
    engineer = Wizard(35, 14, 100)
    bug1 = Enemy(12, 10, 100)
    chest = Chest(7, 9, [Weapon('Knife', 2)])
    screw = Item('Screw', 20, 6)
    
    statusbar.set_character(student)
    world.print_map()

    while True:
        c = raw_input("You > ")
        
        if c == "x":
            break
            # u, d, l, r
        elif c in DIRECTIONS:
            student.move(DIRECTIONS[c])
            bug1.act(student, DIRECTIONS)
        elif c == "a":
            student.attack(bug1)
            bug1.act(student, DIRECTIONS)
        elif c == "gps":
            statusbar.set_status("Your GPS location: %i %i" % (student.x, student.y))
            statusbar.set_status("Bug GPS location: %i %i" % (bug1.x, bug1.y))
        elif c == "i":
            student.show_items()
        elif c == "o":
            student.open()
        elif c.startswith("p"):
            l = c.split()
            if len(l) == 2 and l[-1].isdigit():
                student.pick(int(l[-1]))
            else:
                student.pick()
        elif c.startswith("drop"):
            l = c.split()
            if len(l) == 2 and l[-1].isdigit():
                student.drop(int(l[-1]))
        elif c.startswith("draw"):
            l = c.split()
            if len(l) == 2 and l[-1].isdigit():
                student.draw_weapon(int(l[-1]))
        else:
            statusbar.set_status("Unknown command. 'x' to exit game")
            
        statusbar.show()
        world.print_map()


