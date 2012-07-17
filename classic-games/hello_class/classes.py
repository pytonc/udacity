#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
import random

CHR_PLAYER = "S"
CHR_ENEMY = "B"
CHR_WIZARD = "W"
CHR_ARCHER = "A"
CHR_DEAD = "X"
CHR_FOUNTAIN = "F"
CHR_MONK = "M"
#DIRECTIONS = {"r": "right", "l": "left", "d": "down", "u": "up"}


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


world = WorldMap(60, 22)

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

    def distance_x(self, other):
        return (other.x - self.x)

    def distance_y(self, other):
        return (other.y - self.y)



class Facility(Entity):

    def __init__(self, x, y, amount, image):
        Entity.__init__(self, x, y, image)
        for f in range(amount):
            self.occupy(random.randint(1, world.width-1), random.randint(1, world.height-1))

class Fountains(Facility):
    def __init__(self, x, y, amount, hp=100):
        Facility.__init__(self, x, y, amount, CHR_FOUNTAIN)


    def heal(self, character):
        if self.hp == 0:
            print("I'm deeply sorry, but I'm empty :(")
        else:
            if Player.hp == 0:
                print("I see, you are dead...so sorry! But I can make you alive again!")
                print("But with one condition! You have to promise me you will become an ascetic.")
                print("If you agree, as a first step, you throw away all your items.")
                choice = raw_input("Are you agree?")
                if choice == "Yes":
                    Player.items = []
                    Player.hp = character.max_hp
                    Player.image = CHR_PLAYER
                else:
                    print("Greed kills.")

            else:
                while (self.distance(character) == (0,1) or self.distance(character) == (1,0)):
                    character.hp += 10
                    self.hp -= 10
                    break

class Character(Entity):
    def __init__(self, x, y, image, damage, hp = 100):
        Entity.__init__(self, x, y, image)
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

    def haotic_move(self, directions):
            while (True):
                #It runs away.
                goto = directions[random.choice(directions.keys())]
                new_x, new_y = self.new_pos(goto)
                if not world.is_occupied(new_x, new_y):
                    self.move(goto)
                    break
                break

    def hunt(self, character, directions, steps):
        while self.hp != 0:
            #While alive, enemy, if player is not close enough (if so, it attaks),
            #find where to go to find the player out. Enemy is looking for player until player is in the next cell.
            #Steps here for Wizard, Archer and others. They have their out range for attak

            if self.distance(character) == (0, 1) or self.distance(character) == (1, 0):
                self.attack(character)
                break
            elif (self.distance_x(character) >  steps):
                self.move(directions['r'])
                break
            elif (self.distance_x(character) < -steps):
                self.move(directions['l'])
                break
            elif (self.distance_y(character) >  steps):
                self.move(directions['u'])
                break
            elif (self.distance_y(character) < -steps):
                self.move(directions['d'])
                break
            else:
                self.move(None)
                break

    def attack(self, enemy):

        if self.hp == 0:
            print("Corpses can't attack, unless they are zombies. But you are not.")
        else:
            #dist = self.distance(enemy)
            #if dist == (0, 1) or dist == (1, 0):
            if not enemy.hp:
                msgs = [
                "  This body doesn't look delicious at all.",
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
           # else:
            #    msgs = [
             #       "Woah! Kicking air really is fun!",
              #      "This would be totally ineffective!",
               #     "Just scaring the hiding velociraptors..."
                #    ]
                #statusbar.set_status(random.choice(msgs))


    def condition(self):
        return (self.hp * 100) / self.max_hp

    def harm(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.image = CHR_DEAD
            self.hp = 0

    def get_all_enemies_at_distance(self, dist):
        """Return a list of all enemies that are exactly 'dist' cells away
        either horizontally or vertically.
        """
        coords = [((self.x + dist) % world.width, self.y % world.height),
                  ((self.x - dist) % world.width, self.y % world.height),
                  (self.x % world.width, (self.y + dist) % world.height),
                  (self.x % world.width, (self.y - dist) % world.height)]
        enemies = []
        for x, y in coords:
            if world.is_occupied(x, y) and isinstance(world.map[x][y], Enemy):
                enemies.append(world.map[x][y])
        return enemies

    def get_all_enemies(self, max_dist=1):
        """Return a list of all enemies that are at most 'max_dist' cells away
        either horizontally or vertically.
        """
        enemies = []
        for dist in range(1, max_dist+1):
            enemies.extend(self.get_all_enemies_at_distance(dist))
        return enemies

    def get_alive_enemies_at_distance(self, dist):
        """Return a list of alive enemies that are exactly 'dist' cells away
        either horizontally or vertically.
        """
        enemies = self.get_all_enemies_at_distance(dist)
        return [enemy for enemy in enemies if enemy.hp > 0]

    def get_alive_enemies(self, max_dist=1):
        """Return a list of alive enemies that are at most 'max_dist' cells away
        either horizontally or vertically.
        """
        enemies = self.get_all_enemies(max_dist)
        return [enemy for enemy in enemies if enemy.hp > 0]

class Player(Character):
    def __init__(self, x, y):
        Character.__init__(self, x, y, CHR_PLAYER, damage = 10)

class Enemy(Character):
    def __init__(self, x, y):
        Character.__init__(self, x, y, CHR_ENEMY, damage = 10)

    def challenge(self, other):
        print "Let's fight!"

    def act(self, character, directions):
        # No action if dead X-(
        if not self.hp:
            return False

        choices = [1, 2]
        choice = random.choice(choices)
        #Enemy has poor eyes :(.
        if self.distance_x(character) > 10 or self.distance_x(character) < -10 or self.distance_y(character) > 10 or self.distance_y(character) < -10:
            self.haotic_move(directions)
        else:
            #If character is weak or enemy is strong, without panic.
            if character.hp <= 30 or self.hp > 30:
                self.hunt(character, directions, 1)
            #If it is about to die, it panics
            elif(self.hp <= 30):
                self.haotic_move(directions)

            else:
                #If character and enemy both are about to die, the way, panic or nor, chooses randomly.
                if (character.hp <= 30 and self.hp <= 30):
                    if choice == 1:
                        self.haotic_move(directions)
                    elif choice == 2:
                        self.hunt(character, directions, 1)
                #Any other cases, enemy doesn't panic.
                else:
                    self.hunt(character, directions, 1)



class Minor_Characters(Character):
        def __init__(self, x, y, image, demage):
            Character.__init__(self, x, y, image, demage)

        def act(self, character, directions, steps):
            self.hunt(character, directions, steps)



class Wizard(Minor_Characters):
    def __init__(self, x, y, mana = 100):
        Minor_Characters.__init__(self, x, y, CHR_WIZARD, demage=2)
        self.mana = mana


    def cast_spell(self, name, target):
        """Cast a spell on the given target."""
        if name == 'remove':
            self._cast_about_remove(target)
        elif name == 'hp-stealer':
            self._cast_hp_stealer(target)

    def _cast_about_remove(self, enemy):
        enemy.harm(80)
        self.mana -= 97


    def _cast_hp_stealer(self, enemy):
        enemy.harm(3)
        self.hp += 3
        self.mana-=5


    def act_Wizard(self, character, directions):
        spells = {'remove' : 2, 'hp-stealer': 3}
        costs =  {'remove' : 97, 'hp-stealer': 5}
        spell_to_use = random.choice(spells.keys())
        steps = spells[spell_to_use]
        if not self.hp:
            return False

        if character.hp == 0:
            self.haotic_move(directions)
        elif(self.mana < costs[spell_to_use]):
            self.act(character, directions, 1)
        else:
            if self.distance(character) == (0, steps) or self.distance(character) == (steps, 0):
                self.cast_spell(spell_to_use, character)
            else:
                self.act(character, directions, steps)



class Archer(Minor_Characters):
    def __init__(self, x, y):
        Minor_Characters.__init__(self, x, y, CHR_ARCHER, demage = 3)

    def range_attack(self, enemy):
        dist = self.distance(enemy)
        if (dist[0] <= 5 and dist[1] == 0) or (dist[0] == 0 and dist[1] <= 5):
            enemy.harm(5)

class Monk(Minor_Characters):
    def __init__(self, x, y, mana=100):
        Minor_Characters.__init__(self, x, y, CHR_ENEMY_MONK, demage = 0)
        self.mana = mana

    def heal(self, friend):
        self.hp -= 2
        enemy.hp +=5
        self.mana -=5


