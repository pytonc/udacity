#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects

world = [[None] * 100] * 100

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        world[x][y] = self
    
    def remove(self):
        world[self.x][self.y] = None

class Character(Entity):
    def __init__(self, x, y, hp):
        Entity.__init__(self, x, y)
        self.hp = hp
        self.items = []
    
    def moveLeft(self):
        self.x -= 1
    
    def moveRight(self):
        self.x += 1

    def attack(self, enemy):
        if abs(enemy.x - self.x) == 1 and (enemy.y == self.y):
            enemy.hp -= 10

class Wizard(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, hp)
    
    def castSpell(self, enemy):
        if abs(enemy.x - self.x) == 1 and (enemy.y == self.y):
            enemy.remove()

class Archer(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, hp)
    
    def rangeAttack(self, enemy):
        if abs(enemy.x - self.x) <= 5 and (enemy.y == self.y):
            enemy.hp -= 5

if __name__ == '__main__':
    #initializing some entities
    student = Character(10, 10, 100)
    bug1 = Character(12, 10, 100)
    print """Welcome to 'Hello, Class' game
    Available commands are:
    r - move right
    l - move left
    a - attack
    gps - print location
    
    There is a Bug 2 steps to the right from you.
    You should probably do something about it!
    """

    while True:
        c = raw_input("You > ")
        if c == "exit":
            break
        elif c == "r":
            student.moveRight()
            print "You now are at location: ", student.x, student.y
        elif c =="l":
            student.moveLeft()
        elif c == "gps":
            print "Your GPS location: ", student.x, student.y
            print "Bug GPS location: ", bug1.x, bug1.y
        elif c == "a":
            student.attack(bug1)
            print "Bug now has: ", bug1.hp, " hp left"
        else:
            print "Unknown command. 'exit' to exit the game"


