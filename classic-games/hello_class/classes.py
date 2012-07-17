#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
import random


class WorldMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[None for y in range(self.height)]
                    for x in range(self.width)]

    def is_occupied(self, x, y):
        ''' Checks if a given space on the map and
        returns True if occupied. '''
        return self.map[x][y] is not None


class Entity(object):
    def __init__(self, world_map, x, y):
        self.x = x
        self.y = y
        self.world = world_map

    def occupy(self, x, y):
        self.world.map[x][y] = self

    def remove(self):
        self.world.map[self.x][self.y] = None

    def distance(self, other):
        return abs(other.x - self.x), abs(other.y - self.y)


class Character(Entity):
    def __init__(self, ui, x, y, hp, damage=10):
        Entity.__init__(self, ui.world_map, x, y)
        self.hp, self.max_hp = hp, hp
        self.damage = damage
        self.items = []
        self.ui = ui
        self.world = ui.world_map
        #print "Created character with position x = "
        #        + str(self.x) + " y = " + str(self.y)

    def is_dead(self):
        if self.hp <= 0:
            return True
        return False

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
            dy = -1
        elif direction == 'down':
            dy = 1
        return dx, dy

    def new_pos(self, direction):
        '''
            Calculates a new position given a direction. Takes as input a
            direction 'left', 'right', 'up' or 'down'. Allows wrapping of the
            world map (eg. moving left from x = 0 moves you to x = -1)
        '''
        dx, dy = self._direction_to_dxdy(direction)
        new_x = (self.x + dx) % self.world.width
        new_y = (self.y + dy) % self.world.height
        return new_x, new_y

    def move(self, direction):
        """
            Moves the character to the new position.
        """
        new_x, new_y = self.new_pos(direction)
        if self.world.is_occupied(new_x, new_y):
            self.ui.set_status('Position is occupied, try another move.')
        else:
            self.remove()
            self.x, self.y = new_x, new_y
            self.occupy(self.x, self.y)
            self.ui.draw_window()

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
                self.ui.set_status(random.choice(msgs))
            else:
                # Possible damage is depending on physical condition
                worst = int((self.condition() * 0.01) ** (1 / 2.) * self.damage + 0.5)
                best = int((self.condition() * 0.01) ** (1 / 4.) * self.damage + 0.5)
                damage = (worst == best) and best or random.randrange(worst, best)

                # Possible damage is also depending on sudden adrenaline
                # rushes and aiming accuracy or at least butterfly flaps
                damage = random.randrange(
                    (damage - 1, 0)[not damage],
                    (damage + 1, self.damage)[damage == self.damage])
                enemy.harm(damage)

                if enemy.is_player():
                    self.ui.set_status("You are being attacked: %i damage." % damage)
                elif self.is_player():
                    if enemy.is_dead():
                        self.ui.set_status("You make %i damage: your enemy is dead." % damage)
                    else:
                        self.ui.set_status("You make %i damage: %s has %i/%i hp left." %
                            (damage, enemy.get_label(), enemy.hp, enemy.max_hp))
        else:
            msgs = [
                "Woah! Kicking air really is fun!",
                "This would be totally ineffective!",
                "Just scaring the hiding velociraptors..."
                ]
            self.ui.set_status(random.choice(msgs))

    def condition(self):
        return (self.hp * 100) / self.max_hp

    def harm(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.set_dead()

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
        for dist in range(1, max_dist + 1):
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
    def __init__(self, ui, x, y, hp):
        Character.__init__(self, ui, x, y, hp)


class Enemy(Character):
    def __init__(self, ui, x, y, hp):
        Character.__init__(self, ui, x, y, hp)

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
                if not self.world.is_occupied(new_x, new_y):
                    self.move(goto)
                    break
        elif choice == 2:
            # Fighting back
            self.attack(character)


class Wizard(Character):
    def __init__(self, ui, x, y, hp):
        Character.__init__(self, ui, x, y, hp)

    def _cast_remove(self, enemy):
        dist = self.distance(enemy)
        if dist == (0, 1) or dist == (1, 0):
            enemy.remove()

    def cast_spell(self, name, target):
        """Cast a spell on the given target."""
        if name == 'remove':
            self._cast_remove(target)
        elif name == 'hp-stealer':
            self._cast_hp_stealer(target)
        else:
            print "The wizard does not know the spell '{0}' yet.".format(name)

    def _cast_hp_stealer(self, enemy):
        dist = self.distance(enemy)
        if dist == (0, 3) or dist == (3, 0):
            enemy.harm(3)
            self.hp += 3


class Archer(Character):
    def __init__(self, ui, x, y, hp):
        Character.__init__(self, ui, x, y, hp)

    def range_attack(self, enemy):
        dist = self.distance(enemy)
        if (dist[0] <= 5 and dist[1] == 0) or (dist[0] == 0 and dist[1] <= 5):
            enemy.harm(5)

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
