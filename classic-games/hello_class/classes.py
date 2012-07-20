#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
import random

CHR = {
'CHR_PLAYER'              : "S"     ,
'CHR_ENEMY'               : "B"     ,
'CHR_WIZARD'              : "W"     ,
'CHR_DOG'                 : "D"     ,
'CHR_DEAD'                : "X"     ,
'CHR_FOUNTAIN'            : "F"     ,
'CHR_MONK'                : "M"     ,
'CHR_TREE'                : "T"     ,
'CHR_LEAF'                : "L"     ,
'CHR_GATE'                : "G"     ,
'CHR_WALL'                : "WL"    ,
'CHR_TRAFFIC_LIGHT_RED'   : "TLR"   ,
'CHR_TRAFFIC_LIGHT_GREEN' : "TLG"   ,
'CHR_BUTTERFLY'           : "BF"    ,
'CHR_HOUSE'               : "H"     ,
'CHR_MOUNTAINS'           : "MT"    ,
'CHR_FLAG'                : "FG"
}
DIRECTIONS = ["right", "left", "down", "up"]


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

    def who_is(self, x, y):
        result =[]
        cell = world.map[x][y]
        try:
            for chrs in CHR:
                if CHR[chrs] == cell.image:
                    return CHR[chrs]
        except AttributeError:
            return None

    def around(self, character, cells):
        return (abs(self.distance_x(character)) <= cells and abs(self.distance_y(character)) <= cells )

    def not_around(self, character, cells):
        return abs(self.distance_x(character)) >= cells or abs(self.distance_y(character)) >= cells

    def temp_list(self, l):
        tempList = []
        for e in l:
            tempList.append(e)
        return tempList

class Environment(Entity):
    def __init__(self, x, y, amount, image):
        Entity.__init__(self, x, y, image)
        for f in range(amount):
            self.occupy(random.randint(1, world.width-1), random.randint(1, world.height-1))

class Tree(Environment):
    def __init__(self, x, y, amount):
        Environment.__init__(self, x, y, amount, CHR['CHR_TREE'])

class Leaf_Tree(Environment):
    def __init__(self, x, y, amount):
        Environment.__init__(self, x, y, amount, CHR['CHR_LEAF'])

class Facility(Entity):
    def __init__(self, x, y, image):
        Entity.__init__(self, x, y, image)
        self.occupy(x, y)

class House(Facility):
    def __init__(self, x, y, character):
        Facility.__init__(self, x, y, CHR['CHR_HOUSE'])

    def own(self, character):
        x_house = self.x
        y_house = self.y
        self.occupy(x_house, y_house)

class Gate(Facility):
    def __init__(self, x, y):
        Facility.__init__(self, x, y, CHR['CHR_GATE'])

    def open_close(self, character):
        x_gates = self.x
        y_gates = self.y
        self.occupy(x_gates, y_gates)

class Wall(Facility):
    def __init__(self, x, y):
        Facility.__init__(self,x, y, CHR['CHR_WALL'])
        fu,fd,su,sd,b = 1,1,1,1,1

        for front_up in range(4):
            self.occupy(x, y+fu)
            fu+=1
        for front_down in range(4):
            self.occupy(x, y-2-fd)
            fd+=1
        for side_up in range(10):
            self.occupy(x-su,y+4)
            su+=1
        for side_down in range(10):
            self.occupy(x-sd,y-6)
            sd+=1
        for back in range(10):
            self.occupy(x-10, y+4-b)
            b+=1

class Traffic_Light(Facility):
    def __init__(self, x, y):
        Facility.__init__(self, x, y, CHR['CHR_TRAFFIC_LIGHT_RED'])

    def work(self, character):
        while True:
            if ((self.distance(character) == (0,1) or self.distance(character) == (1,0)) or self.distance(character) == (1,1)):
               self.image = CHR['CHR_TRAFFIC_LIGHT_GREEN']
               break
            else:
               self.image = CHR['CHR_TRAFFIC_LIGHT_RED']
               break

class Fountains(Facility):
    def __init__(self, x, y, hp=100):
        Facility.__init__(self, x, y, CHR['CHR_FOUNTAIN'])
        self.hp = hp

    def heal(self, character):
        while True:
            if (self.distance(character) == (0,1) or self.distance(character) == (1,0)) or self.distance(character) == (1,1):
                if self.hp <= 0:
                    print("I'm deeply sorry, but I'm empty :(")
                    break
                else:
                    if(character.hp < character.max_hp and character.hp != 0):
                        character.hp += 10
                        self.hp -= 10
                        break
                    elif(character.hp >= character.max_hp):
                        print "You don't need medical aid, fraud!"
                        break
                    elif(character.hp == 0):
                        print("I see, you are dead...so sorry! But I can make you alive again!")
                        print("But with one condition! You have to promise me you will become an ascetic.")
                        print("If you agree, as a first step, you throw away all your items.")
                        choice = raw_input("Are you agree?")
                        if choice == "Yes":
                            character.items = []
                            character.hp = character.max_hp
                            character.image = CHR['CHR_PLAYER']
                            self.hp -= 100
                        break
            else:
                return None
                break

class Mountain(Facility):
    def __init__(self, x, y):
        Facility.__init__(self, x, y, CHR['CHR_MOUNTAINS'])
        mt_f, mt_s = 1, 1
        for mountains in range(world.height/2 - 2):
            self.occupy(x,y + mt_f)
            mt_f+=1
        for mountains in range(world.height/2 - 2):
            self.occupy(x, world.height - mt_s)
            mt_s +=1

class Flag(Facility):
    def __init__(self, x, y):
        Facility.__init__(self, x, y, CHR['CHR_FLAG'])
        self.occupy(3 * world.width/4, world.height/2 - 1)

class Character(Entity):
    def __init__(self, x, y, image, damage, hp = 100, hp_max = 100):
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
        temp_directions = self.temp_list(DIRECTIONS)
        random.shuffle(temp_directions)

        if (world.is_occupied(new_x, new_y)):
            if (len(temp_directions) != 0):
                for direction_to_go in temp_directions:
                    if not world.is_occupied(self.new_pos(direction_to_go)[0], self.new_pos(direction_to_go)[1]):
                        self.move(direction_to_go)
                    else:
                        temp_directions.remove(direction_to_go)
            else:
                self.stay()

        else:
            self.remove()
            self.x, self.y = new_x, new_y
            self.occupy(self.x, self.y)

    def move_player(self, direction, exception):
        new_x, new_y = self.new_pos(direction)
        if (exception[0] == self.who_is(new_x, new_y) or exception[1] == self.who_is(new_x, new_y)):
            self.remove()
            self.x, self.y = new_x, new_y
            self.occupy(self.x, self.y)
        else:
            self.move(direction)

    def stay(self):
        self.move(None)

    def haotic_move(self, directions):
            while (True):
                #It runs away.
                goto = directions[random.choice(directions.keys())]
                new_x, new_y = self.new_pos(goto)
                if not world.is_occupied(new_x, new_y):
                    self.move(goto)
                    break

    def hunt(self, character, directions, steps):
        while True:
            #While alive, enemy, if player is not close enough (if so, it attaks),
            #find where to go to find the player out. Enemy is looking for player until player is in the next cell.
            #Steps here for Wizard, Archer and others. They have their out range for attak
            if self.distance(character) == (0, 1) or self.distance(character) == (1, 0) or self.distance(character) == (1, 1):
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
                self.stay()
                break

    def follow(self, character, directions, steps):     #The same as hunt, but without attacking. One step from delict! :)
        while True:
            if (self.distance_x(character) >  steps):
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
                self.stay()
                break

    def attack(self, enemy):

        if self.hp == 0:
            print("Corpses can't attack, unless they are zombies. But you are not.")
        else:
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
                damage = (worst == best) and best or random.randint(worst, best)

                    # Possible damage is also depending on sudden adrenaline
                    # rushes and aiming accuracy or at least butterfly flaps
                damage = random.randint(
                        (damage-1, 0)[not damage],
                        (damage+1, self.damage)[damage == self.damage])
                enemy.harm(damage)

                if enemy.image == CHR['CHR_PLAYER']:
                    statusbar.set_status("You are being attacked: %i damage." % damage)
                elif self.image == CHR['CHR_PLAYER']:
                    if enemy.image == CHR['CHR_DEAD']:
                        statusbar.set_status("You make %i damage: your enemy is dead." % damage)
                    else:
                        statusbar.set_status("You make %i damage: %s has %i/%i hp left." %
                            (damage, enemy.image, enemy.hp, enemy.max_hp))

    def condition(self):
        return (self.hp * 100) / self.max_hp

    def harm(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.image = CHR['CHR_DEAD']
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

    def get_all_enemies(self, max_dist):
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

    def get_alive_enemies(self, max_dist):
        """Return a list of alive enemies that are at most 'max_dist' cells away
        either horizontally or vertically.
        """
        enemies = self.get_all_enemies(max_dist)
        return [enemy for enemy in enemies if enemy.hp > 0]

    def get_alive_enemies_around(self, enemies, cells):
        existance = []
        boolean = False
        for character in enemies:
            if self.around(character, cells): #and character.hp != 0:
                existance.append(character)
                boolean = True
        return existance, boolean

class Player(Character):
    def __init__(self, x, y):
        Character.__init__(self, x, y, CHR['CHR_PLAYER'], damage = 10)

class Enemy(Character):
    def __init__(self, x, y):
        Character.__init__(self, x, y, CHR['CHR_ENEMY'], damage = 10)

    def challenge(self, other):
        print "Let's fight!"

    def act(self, character, directions):
        # No action if dead X-(
        if not self.hp:
            return False

        choices = [1, 2]
        choice = random.choice(choices)
        #Enemy has poor eyes :(.
        if self.not_around(character, 10)  or character.hp == 0:
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
        def __init__(self, x, y, image, damage):
            Character.__init__(self, x, y, image, damage)

        def act(self, character, directions, steps):
            self.hunt(character, directions, steps)

        def walk(self, directions):
            self.haotic_move(directions)

class Butterfly(Minor_Characters):
    def __init__(self, x, y, hp = 20):
        Minor_Characters.__init__(self, x, y, CHR['CHR_BUTTERFLY'], damage=1)
        self.hp = hp

    def fly(self, character, directions):
        while True:
            if self.around(character, 2):
                new_x = (self.x + random.randint(-3,3))  % world.width
                new_y = (self.y + random.randint(-3,3))  % world.height
                if world.is_occupied(new_x, new_y):
                    self.move(random.choice(directions.keys()))
                    break
                else:
                    self.remove()
                    self.x, self.y = new_x, new_y
                    self.occupy(self.x, self.y)
                    break
            else:
                self.haotic_move(directions)

class Car(Minor_Characters):
    def __init__(self, x, y, image ):
        Minor_Characters.__init__(self, x, y, image, damage=0)

class Wizard(Minor_Characters):
    def __init__(self, x, y, mana = 100):
        Minor_Characters.__init__(self, x, y, CHR['CHR_WIZARD'], damage=2)
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
            self.walk(directions)
        elif(self.mana < costs[spell_to_use]):
            self.act(character, directions, 1)
        else:
            if self.distance(character) == (0, steps) or self.distance(character) == (steps, 0) or self.distance(character) == (steps, steps):
                self.cast_spell(spell_to_use, character)
            else:
                self.act(character, directions, steps)

class Dog(Minor_Characters):
    def __init__(self, x, y):
        Minor_Characters.__init__(self, x, y, CHR['CHR_DOG'], damage = 7)

    def act_Dog(self, owner, enemies, directions):
        if self.hp <= 0:
                return False

        existance = self.get_alive_enemies_around(enemies, 3)

        if owner.hp <= 0:
            self.hp -= 50
            if enemies[0].hp !=0:
                self.act(enemies[0], directions, 1)
            elif enemies[1].hp !=0:
                self.act(enemies[1], directions, 1)
            else:
                self.walk(directions)
        else:
            if existance[1]:
                self.act(random.choice(existance[0]), directions, 1)
            else:
                self.follow(owner, directions, 1)

class Monk(Minor_Characters):
    def __init__(self, x, y, mana=100):
        Minor_Characters.__init__(self, x, y, CHR['CHR_MONK'], damage = 0)
        self.mana = mana

    def heal(self, friend):
        self.hp -= 2
        friend.hp +=5
        self.mana -=5

    def act_Monk(self, friend, directions):
        if self.mana >= 5:
            if self.around(friend, 10):
                if friend.hp < friend.max_hp and friend.hp != 0:
                    self.heal(friend)
                else:
                    self.walk(directions)
            else:
                self.walk(directions)
        else:
            self.walk(directions)

