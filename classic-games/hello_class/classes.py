#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
class WorldMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[None for y in range(self.height)] for x in range(self.width)]

    def is_occupied(self, x, y):
        ''' Checks if a given space on the map and returns True if occupied. '''
        return self.map[x][y] is not None

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

world = WorldMap(50, 22)

#world = [[None for x in range(100)] for y in range(100)]

class Entity:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        world.map[x][y] = self
        self.image = image
    
    def occupy(self, x, y):
        world.map[x][y] = self

    def remove(self):
        world.map[self.x][self.y] = None

    def distance(self, other):
        return abs(other.x - self.x), abs(other.y - self.y)

class Character(Entity):
    def __init__(self, x, y, image, hp):
        Entity.__init__(self, x, y, image)
        self.hp = hp
        self.items = []

    def _direction_to_dxdy(self, direction):
        """Convert a string representing movement direction into a tuple
        (dx, dy), where 'dx' is the size of step in the 'x' direction and
        'dy' is the size of step in the 'y' direction."""
        dx, dy = 0, 0
        if direction == 'left':
            dx = -1
        elif direction == 'right':
            dx = 1
        elif direction == 'up':
            dy = 1
        elif direction == 'down':
            dy = -1
        else:
            print "Please enter a valid direction: 'left', 'right', 'up', or 'down'"
        return dx, dy

    def move(self, direction):
        '''
            Moves a character one space in a given direction. Takes as input a 
            direction 'left', 'right', 'up' or 'down'. Allows wrapping of the 
            world map (eg. moving left from x = 0 moves you to x = -1)
        '''
        dx, dy = self._direction_to_dxdy(direction)
        new_x = (self.x + dx) % world.width
        new_y = (self.y + dy) % world.height
        if world.is_occupied(new_x, new_y):
            print 'Position is occupied, try another move.'
        else:
            self.remove()
            self.x, self.y = new_x, new_y
            self.occupy(self.x, self.y)

    def attack(self, enemy):
        dist = self.distance(enemy)
        if dist == (0, 1) or dist == (1, 0):
            enemy.harm(10)

    def harm(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.image = 'X'
            self.hp = 0

class Enemy(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, 'B', hp)

    def challenge(self, other):
        print "Let's fight!"

class Wizard(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, 'W', hp)
    
    def cast_spell(self, enemy):
        dist = self.distance(enemy)
        if dist == (0, 1) or dist == (1, 0):
            enemy.remove()

class Archer(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, 'A', hp)
    
    def range_attack(self, enemy):
        dist = self.distance(enemy)
        if (dist[0] <= 5 and dist[1] == 0) or (dist[0] == 0 and dist[1] <= 5):
            enemy.harm(5)
