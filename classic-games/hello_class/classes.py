#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects

# Hacked by MikeGoldberg to use Pygame
# Mon Jul 16 12:51:31 CDT 2012

import random
import pygame


CHR_PLAYER = "S"
CHR_ENEMY = "B"
CHR_WIZARD = "W"
CHR_ARCHER = "A"
CHR_DEAD = "X"

# Pygame constants
WORLD_MAX_H = 60
WORLD_MAX_V = 22
BLOCK_SIZE = 10
COLOR_PLAYER = (0, 0, 255)
COLOR_ENEMY = (255, 0, 0)
COLOR_WIZARD = (0, 255, 0)
COLOR_ARCHER = (255, 0, 255)
COLOR_DEAD = (0, 0, 0)

class StatusBar(object):
    def __init__(self, character = None):
        self.character = character
        self.msg = ''

    def set_character(self, character):
        self.character = character
        self.set_status()
        self.show()

    def set_status(self, msg = ''):
        self.msg = (msg, '::'.join((self.msg, msg)))[len(self.msg) > 0]
        print self.character.hp
        print self.character.max_hp

        status = "HP: %i/%i" % (self.character.hp, self.character.max_hp)
        msgs = self.msg.split('::')

        self.line1 = "%s + %s" % (status, msgs[0])
        if len(msgs) > 1:
            self.line2 = "%s + %s" % (' ' * len(status), msgs[1])
        else:
            self.line2 = "%s + %s" % (' ' * len(status), ' ' * len(msgs[0]))


    def format_line(self, txt, width):
        line = "+ %s" % txt
        line += " " * (width - (len(line))) + " +"
        return line

    def show(self):
        self.set_status()
        print "+" * (world.width + 2)
        print self.format_line(self.line1, world.width)
        print self.format_line(self.line2, world.width)
        self.msg = ''

statusbar = StatusBar()

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

world = WorldMap(WORLD_MAX_H, WORLD_MAX_V)

#world = [[None for x in range(100)] for y in range(100)]

class Entity:
    def __init__(self, x, y, image, screen):
        print 'Entity',x,y,image,screen
        self.x = x
        self.y = y
        world.map[x][y] = self
        self.image = image

        # Pygame sprite initialization
        if image == 'S':
            self.sprite_color = COLOR_PLAYER
        elif image == 'B':
            self.sprite_color = COLOR_ENEMY
        elif image == 'W':
            self.sprite_color = COLOR_WIZARD
        elif image == 'A':
            self.sprite_color = COLOR_ARCHER
        else:
            self.sprite_color = COLOR_DEAD
        self.sprite = pygame.Surface((BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        self.sprite.fill(self.sprite_color)
        self.screen = screen
        self.screen.blit(self.sprite, (10*self.x, 21*self.y))

    def occupy(self, x, y):
        world.map[x][y] = self

    def remove(self):
        world.map[self.x][self.y] = None

    def distance(self, other):
        return abs(other.x - self.x), abs(other.y - self.y)

class Character(Entity):
    def __init__(self, x, y, image, screen, hp, damage = 10 ):
        print 'Character', x,y,image,screen,hp
        print 'type(screen)', type(screen)
        Entity.__init__(self, x, y, image, screen)
        self.hp, self.max_hp = hp, hp
        self.damage = damage
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
        return dx, dy

    def new_pos(self, direction):
        '''
            Calculates a new position given a direction. Takes as input a
            direction 'left', 'right', 'up' or 'down'. Allows wrapping of the
            world map (eg. moving left from x = 0 moves you to x = -1)
        '''
        dx, dy = self._direction_to_dxdy(direction)
        new_x = (self.x + dx) % world.width
        new_y = (self.y + dy) % world.height
        return new_x, new_y

    def move(self, direction):
        """
            Moves the character to the new position.
        """
        new_x, new_y = self.new_pos(direction)
        if world.is_occupied(new_x, new_y):
            statusbar.set_status('Position is occupied, try another move.')
        else:
            self.remove()
            self.x, self.y = new_x, new_y
            self.occupy(self.x, self.y)

    def attack(self, enemy):
        dist = self.distance(enemy)
        if dist == (0, 1) or dist == (1, 0):
            if not enemy.hp:
                msgs = [
                    "This body doesn't look delicious at all.",
                    "You really want me to do this?",
                    "Yeah, whatever!",
                    "I killed it! What did you make me do!"
                    ]
                statusbar.set_status(random.choice(msgs))
            else:
                # Possible damage is depending on physical condition
                worst = int((self.condition() * 0.01) ** (1/2.) * self.damage + 0.5)
                best = int((self.condition() * 0.01) ** (1/4.) * self.damage + 0.5)
                damage = (worst == best) and best or random.randrange(worst, best)

                # Possible damage is also depending on sudden adrenaline
                # rushes and aiming accuracy or at least butterfly flaps
                damage = random.randrange(
                    (damage-1, 0)[not damage],
                    (damage+1, self.damage)[damage == self.damage])
                enemy.harm(damage)

                if enemy.image == CHR_PLAYER:
                    statusbar.set_status("You are being attacked: %i damage." % damage)
                elif self.image == CHR_PLAYER:
                    if enemy.image == CHR_DEAD:
                        statusbar.set_status("You make %i damage: your enemy is dead." % damage)
                    else:
                        statusbar.set_status("You make %i damage: %s has %i/%i hp left." % \
                            (damage, enemy.image, enemy.hp, enemy.max_hp))
        else:
            msgs = [
                "Woah! Kicking air really is fun!",
                "This would be totally ineffective!",
                "Just scaring the hiding velociraptors..."
                ]
            statusbar.set_status(random.choice(msgs))


    def condition(self):
        return (self.hp * 100) / self.max_hp

    def harm(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.image = CHR_DEAD
            self.hp = 0

class Player(Character):
    def __init__(self, x, y, screen, hp):
        Character.__init__(self, x, y, CHR_PLAYER, screen, hp)

class Enemy(Character):
    def __init__(self, x, y, screen, hp):
        Character.__init__(self, x, y, CHR_ENEMY, screen, hp)

    # not used
    def challenge(self, other):
        print "Let's fight!"

    def act(self, character, directions):
        # No action if dead X-(
        if not self.hp:
            return False

        choices = [0, 1]

        dist = self.distance(character)
        if dist == (0, 1) or dist == (1, 0):
            choices.append(2)
        choice = random.choice(choices)

        if choice == 1:
            # Running away
            while (True):
                goto = directions[random.choice(directions.keys())]
                new_x, new_y = self.new_pos(goto)
                if not world.is_occupied(new_x, new_y):
                    self.move(goto)
                    break
        elif choice == 2:
            # Fighting back
            self.attack(character)

class Wizard(Character):
    def __init__(self, x, y, screen, hp):
        Character.__init__(self, x, y, CHR_WIZARD, screen, hp)

    def cast_spell(self, enemy):
        dist = self.distance(enemy)
        if dist == (0, 1) or dist == (1, 0):
            enemy.remove()

    def cast_hp_stealer(self, enemy):
        dist = self.distance(enemy)
        if dist == (0,3) or dist == (0,3):
            enemy.harm(3)
            self.hp += 3

class Archer(Character):
    def __init__(self, x, y, screen, hp):
        Character.__init__(self, x, y, CHR_ARCHER, screen, hp)

    def range_attack(self, enemy):
        dist = self.distance(enemy)
        if (dist[0] <= 5 and dist[1] == 0) or (dist[0] == 0 and dist[1] <= 5):
            enemy.harm(5)
