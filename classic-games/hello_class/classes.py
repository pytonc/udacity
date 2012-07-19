#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
import random
from lib import *

import pygame
from pygame.locals import *

DIRECTIONS = {
    K_LEFT: (-1, 0),
    K_RIGHT: (1, 0),
    K_UP: (0, -1),
    K_DOWN: (0, 1)
}

# Window constants
GAME_TITLE = "Bug Hunt"

WIDTH = 900
HEIGHT = 600

# Status bar
STATUS_HEIGHT = 50

# Field/Step size
# Images should be of same size 
DIST = 30

# Initialising screen
pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT + STATUS_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
screen = pygame.display.get_surface()

# Standard font
myfont = pygame.font.SysFont("Arial", 18)

# Pre-Loading used images
CHR_PLAYER = pygame.image.load('img/student.png')
CHR_ENEMY = pygame.image.load('img/bug.png')
CHR_WIZARD = pygame.image.load('img/wizard.png')
CHR_DEAD = pygame.image.load('img/dead.png')
CHR_CHEST = pygame.image.load('img/chest.png')
CHR_SWORD = pygame.image.load('img/sword.png')
CHR_POTION = pygame.image.load('img/potion.png')
# for unspecified items
CHR_ITEM = pygame.image.load('img/item.png')

background = pygame.image.load('img/papier.png')

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

INVENTORY_SIZE = 10

    
class Frame(object):
    def __init__(self, color, rect, visible = False):
        self.visible = visible
        self.color = color
        self.rect = rect
        self.content = []
            
    def show(self, val):
        self.visible = val

class Help(Frame):
    def __init__(self, character = None):
        rect = (20, 20, WIDTH - 40, HEIGHT + STATUS_HEIGHT - 40)
        color = (200,200,150)
        
        Frame.__init__(self, color, rect)
        
    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 1)
    
            title = myfont.render("Hilfe", 1, BLACK)
            screen.blit(title, ((WIDTH - title.get_width()) / 2, 40))
    
            lines = []
            lines.append(["<right>", "move right"])
            lines.append(["<left>", "move left"])
            lines.append(["<up>", "move up"])
            lines.append(["<down>", "move down"])
            lines.append(["a", "attack"])
            lines.append(["h", "show / close help"])
            lines.append(["i", "show / close inventory"])
            lines.append(["o", "open / close chest"])
            lines.append(["p", "pick something up"])
            lines.append(["Lft Mouse", "show item infos (inventory)"])
            lines.append(["Rgt Mouse", "pick item (chest) / popup item menu (inventory)"])
            lines.append(["Esc", "exit"])
            
            for line in lines:
                lft = myfont.render(line[0], 1, BLACK)
                rgt = myfont.render(line[1], 1, BLACK)
                y = 60 + title.get_height() + (lft.get_height() + 10) * lines.index(line)
                screen.blit(lft, (100, y))
                screen.blit(rgt, (300, y))
    
class Status(Frame):
    def __init__(self, character = None):
        rect = (0, 0, WIDTH, STATUS_HEIGHT)
        color = (255, 255, 255)
        
        Frame.__init__(self, color, rect, visible = True)
        
        self.character = character
        self.enemy = False

    def set_character(self, character):
        self.character = character
    
    def set_enemy_status(self, enemy):
        self.enemy = enemy
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
        text_hp = myfont.render("HP:", 1, BLACK)
        screen.blit(text_hp, (10, 10))

        hp_bar = 200
        pygame.draw.rect(screen, WHITE, (text_hp.get_width() + 20, 10, hp_bar, 20))
        pygame.draw.rect(screen, RED, (text_hp.get_width() + 20, 10, self.character.condition() * 2, 20))
        pygame.draw.rect(screen, BLACK, (text_hp.get_width() + 20, 10, hp_bar, 20), 2)

        dmg = self.character.damage
        if self.character.weapon:
            dmg += self.character.weapon.damage
            
        text_dmg = myfont.render("Dmg: %s" % dmg, 1, BLACK)
        screen.blit(text_dmg, (text_hp.get_width() + 30 + hp_bar, 10))
        
        # shows enemy hp
        if self.enemy:
            x = text_hp.get_width() + 60 + hp_bar + text_dmg.get_width()
            text_enemy = myfont.render("%s:" % self.enemy.__class__.__name__, 1, BLACK)
            screen.blit(text_enemy, (x, 10))
            pygame.draw.rect(screen, WHITE, (x + text_enemy.get_width() + 10, 10, hp_bar, 20))
            pygame.draw.rect(screen, RED, (x + text_enemy.get_width() + 10, 10, self.enemy.condition() * 2, 20))
            pygame.draw.rect(screen, BLACK, (x + text_enemy.get_width() + 10, 10, hp_bar, 20), 2)
            

statustext = Status()

class Inventory(Frame):
    def __init__(self, rect, title):
        color = (200,200,150)
        Frame.__init__(self, color, rect)
        
        self.width = rect[2]
        self.padding = 40
        self.title = title
        self.selected = False
        self.selection = False
        
    def draw_background(self):
        bg = pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        
        title = myfont.render(self.title, 1, BLACK)
        screen.blit(title, ((self.rect[2] - title.get_width()) / 2 + self.rect[0], self.rect[1] + 10))
        
class ChestInventory(Inventory):
    def __init__(self):
        rect = (20, STATUS_HEIGHT + 20, WIDTH / 2 - 40, HEIGHT - 40)
        Inventory.__init__(self, rect, 'Chest')

    def draw(self):
        if self.visible:
            self.draw_background()
        
            if len(self.items):
                img_width, img_height = self.items[0].sprite.get_width(), self.items[0].sprite.get_height()
                cols = get_cols(self.width, self.padding, img_width)
                
                match = False
                for i in range(len(self.items)):
                    # layout
                    x = self.rect[0] + self.padding + i % cols * (self.padding + img_width)
                    y = self.rect[1] + self.padding + i / cols * (self.padding + img_height)
                    pygame.draw.rect(screen, WHITE, (x, y, img_width, img_height))
                    pygame.draw.rect(screen, BLACK, (x, y, img_width, img_height), 1)
                    screen.blit(self.items[i].sprite, (x, y))
                    
                    # right clicked
                    if self.selection:
                        pos = self.selection
                        
                        # clicked on item
                        if (pos[0] > x and pos[0] < x + img_width) \
                            and (pos[1] > y and pos[1] < y + img_height):
                            match = self.items[i]
            
                # selected item
                self.selected = match
                
                # actual transaction
                if self.selected and self.character:
                    self.character.items.append(self.selected)
                    self.chest.items.remove(self.selected)
                    self.character = False
                    self.selected = False
                
    def set_chest(self, chest):
        """
            Links a chest to the inventory.
        """
        self.chest = chest
        self.items = chest.items
        self.visible = not self.visible
        
    def transact(self, pos, character):
        self.selection = pos
        self.character = character

chest_inventory = ChestInventory()

class MyInventory(Inventory):
    def __init__(self, character):
        rect = (WIDTH / 2 + 20, STATUS_HEIGHT + 20, WIDTH / 2 - 40, HEIGHT - 40)
        Inventory.__init__(self, rect, 'Inventory')
        self.character = character
        
        self.menu = False

    def draw(self):
        self.items = self.character.items
        if self.visible:
            self.draw_background()
        
            if len(self.items):
                img_width, img_height = self.items[0].sprite.get_width(), self.items[0].sprite.get_height()
                cols = get_cols(self.width, self.padding, img_width)
        
                match = False
                for i in range(len(self.items)):
                    # layout
                    x = self.rect[0] + self.padding + i % cols * (self.padding + img_width)
                    y = self.rect[1] + self.padding + i / cols * (self.padding + img_height)
                    pygame.draw.rect(screen, WHITE, (x, y, img_width, img_height))
                    
                    # highlight equipped weapon
                    if isinstance(self.items[i], Weapon) \
                        and self.character.weapon == self.items[i]:
                        pygame.draw.rect(screen, RED, (x, y, img_width, img_height), 3)
                    else:
                        pygame.draw.rect(screen, BLACK, (x, y, img_width, img_height), 1)
                    screen.blit(self.items[i].sprite, (x, y))
                    
                    # right or left clicked
                    if self.menu or self.selection:
                        pos = self.menu or self.selection
                        
                        # check if clicked on item
                        if (pos[0] > x and pos[0] < x + img_width) \
                            and (pos[1] > y and pos[1] < y + img_height):
                            match = self.items[i]
                            pygame.draw.rect(screen, YELLOW, (x, y, img_width, img_height), 3)
            
                # selected item
                self.selected = match
    
                if self.selected:
                    self.info_box()
                    
                    # right clicked
                    if self.menu:
                        rect = (self.menu[0]-100, self.menu[1]-50, 100, 100)
                        pygame.draw.rect(screen, self.color, rect)
                        pygame.draw.rect(screen, BLACK, rect, 1)
                        self.set_choices()
                
                # right clicked but not on item
                if self.menu and not self.selected:
                    self.menu = False
                     
    def info_box(self):
        """
            Shows infos to the clicked item.
        """
        x = WIDTH / 4 - 50
        y = STATUS_HEIGHT + 20
        width = 150
        height = 200
        pygame.draw.rect(screen, self.color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 1)
        
        img_x = width / 2 - self.selected.sprite.get_width() / 2
        img_y = 10
        img_width, img_height = self.selected.sprite.get_size()
        pygame.draw.rect(screen, WHITE, (x + img_x, y + img_y, img_width, img_height))
        pygame.draw.rect(screen, BLACK, (x + img_x, y + img_y, img_width, img_height), 1)
        screen.blit(self.selected.sprite, (x + img_x, y + img_y))
        
        attrs = []
        
        # weapon attributes
        if isinstance(self.selected, Weapon):
            attrs.append(['Dmg', "+ %s" % self.selected.damage])
            attrs.append(['Range', str(self.selected.attack_range)])
            
            # highlight image if weapon is equipped
            if self.character.weapon == self.selected:
                pygame.draw.rect(screen, RED, (x + img_x, y + img_y, img_width, img_height), 3)
        
        # potion attributes
        if isinstance(self.selected, Potion):
            attrs.append(['Hp', "+ %i%%" % int(self.selected.hp * 100)])
        
        # write name
        text_name = myfont.render(self.selected.name, 1, BLACK)
        name_x = width / 2 - text_name.get_width() / 2
        name_y = 10
        screen.blit(text_name, (x + name_x, name_y + img_y + img_height + y))
        
        # write attributes
        for line in attrs:
            text = myfont.render("%s:" % line[0], 1, BLACK)
            text_x = x + 10
            text_y = y + img_y + img_width + name_y + (10 + text.get_height()) * (attrs.index(line) + 1)
            screen.blit(text, (text_x, text_y))
            
            text = myfont.render(line[1], 1, BLACK)
            text_x = x + width - 10 - text.get_width()
            screen.blit(text, (text_x, text_y))
        
    def select_item(self, pos):
        self.selection = pos
    
    def set_choices(self):
        """
            Sets the choices in the item menu.
        """
        padding = 10
        choices = []
        # special choices
        if isinstance(self.selected, Weapon):
            if self.character.weapon == self.selected:
                choices.append('Unequip')
            else:
                choices.append('Equip')
        elif isinstance(self.selected, Potion):
            choices.append('Drink')
        
        # general choices
        choices.append('Drop')
        
        lbls = [myfont.render(lbl, 1, (0,0,0)) for lbl in choices]
        
        pos = self.menu
        for lbl in lbls:
            x = pos[0] - 100 + padding
            y = pos[1] + lbls.index(lbl) * (lbl.get_height() + padding) - 50 + padding
            screen.blit(lbl, (x, y))

            # if left clicked
            if self.selection:
                # check if clicked on choice (lbl)
                if (self.selection[0] > x and self.selection[0] < x + lbl.get_width()) \
                    and (self.selection[1] > y and self.selection[1] < y + lbl.get_height()):
                    
                    # handling choice
                    if choices[lbls.index(lbl)] == 'Equip':
                        self.character.draw_weapon(self.selected)
                    elif choices[lbls.index(lbl)] == 'Unequip':
                        self.character.draw_weapon(False)
                    elif choices[lbls.index(lbl)] == 'Drop':
                        self.character.drop(self.selected)
                    elif choices[lbls.index(lbl)] == 'Drink':
                        self.character.drink(self.selected)

        # if item menu is active and left clicked
        if self.menu and self.selection:
            self.selection = False
            self.selected = False
            self.menu = False
    
    def show_menu(self, pos):
        self.menu = pos
        self.selection = False
        

class WorldMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[None for y in range(self.height)] for x in range(self.width)]

    def is_occupied(self, x, y):
        ''' Checks if a given space on the map and returns True if occupied. '''
        return self.map[x][y] is not None
        
world = WorldMap(WIDTH / DIST, HEIGHT / DIST)

class Entity:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.sprite = image
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
               
        if x and y:
            self.occupy()
    
    def occupy(self):
        world.map[self.x][self.y] = self

    def remove(self):
        world.map[self.x][self.y] = None

    def distance(self, other):
        return abs(other.x - self.x), abs(other.y - self.y)

class Item(Entity):
    def __init__(self, name, x = None, y = None, image = CHR_ITEM):
        Entity.__init__(self, x, y, image)
        self.name = name

class Potion(Item):
    def __init__(self, x = None, y = None):
        Item.__init__(self, 'Health Potion', x, y, CHR_POTION)
        self.hp = 0.5

class Weapon(Item):
    def __init__(self, name, damage, attack_range = 1, x = None, y = None, image = CHR_ITEM):
        Item.__init__(self, name, x, y, image)
        self.damage = damage
        # not yet used
        self.attack_range = attack_range
        
class Sword(Weapon):
    def __init__(self, name, damage, attack_range = 1, x = None, y = None):
        Weapon.__init__(self, name, damage, attack_range, x, y, CHR_SWORD)

class Chest(Entity):
    def __init__(self, x, y, items = []):
        Entity.__init__(self, x, y, CHR_CHEST)
        self.items = items
        
    def open(self):
        chest_inventory.set_chest(self)

class Character(Entity):
    def __init__(self, x, y, image, hp, damage = 10):
        Entity.__init__(self, x, y, image)
        self.hp, self.max_hp = hp, hp
        self.damage = damage
        self.items = []

    def new_pos(self, direction):
        '''
            Calculates a new position given a direction. Takes as input a 
            direction 'left', 'right', 'up' or 'down'. Allows wrapping of the 
            world map (eg. moving left from x = 0 moves you to x = -1)
        '''
        x = direction[0]
        y = direction[1]
        new_x = self.x
        new_y = self.y
        if self.x + x >= 0 and self.x + x < world.width:
            new_x += x
        if self.y + y >= 0 and self.y + y < world.height:
            new_y += y
        return new_x, new_y

    def move(self, direction):
        """
            Moves the character to the new position.
        """
        # No action if dead X-(
        if not self.hp:
            return False
        
        new_x, new_y = self.new_pos(direction)
        if not world.is_occupied(new_x, new_y):
            self.remove()
            self.x, self.y = new_x, new_y
            self.occupy()
            
            if isinstance(self, Player):
                for direction in DIRECTIONS.values():
                    new_x, new_y = self.new_pos(direction)
                    if world.is_occupied(new_x, new_y) \
                        and isinstance(world.map[new_x][new_y], Enemy) \
                        and world.map[new_x][new_y].hp:
                        statustext.set_enemy_status(world.map[new_x][new_y])
                        break
                    else:
                        statustext.set_enemy_status(False)
        
    def attack(self, enemy = None):
        # No action if dead X-(
        if not self.hp:
            return False
        
        if not enemy:
            for value in DIRECTIONS.values():
                x, y = self.new_pos(value)
                if world.is_occupied(x, y) \
                    and isinstance(world.map[x][y], Enemy):
                    if world.map[x][y].hp:
                        enemy = world.map[x][y]
                        break
                    else:
                        continue
            if not enemy:
                return False
        
        dist = self.distance(enemy)
        if dist == (0, 1) or dist == (1, 0):
            if enemy.hp:
                # Possible damage is depending on physical condition
                worst = int((self.condition() * 0.01) ** (1/2.) * self.damage + 0.5)
                best = int((self.condition() * 0.01) ** (1/4.) * self.damage + 0.5)
                damage = (worst == best) and best or random.randint(worst, best)
                
                # Possible damage is also depending on sudden adrenaline
                # rushes and aiming accuracy or at least butterfly flaps
                damage = random.randint(
                    (damage-1, 0)[not damage],
                    (damage+1, self.damage)[damage == self.damage])
                    
                # Check if character class has weapon attribute and character uses a weapon
                if hasattr(self, 'weapon') and self.weapon:
                    damage += self.weapon.damage
                    
                enemy.harm(damage)
            
                if isinstance(self, Player):
                    if isinstance(enemy, Enemy) \
                        and enemy.hp:
                        statustext.set_enemy_status(enemy)
                    else:
                        statustext.set_enemy_status(False)

    def condition(self):
        return (self.hp * 100) / self.max_hp

    def harm(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.sprite = CHR_DEAD
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
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, CHR_PLAYER, hp)
        self.weapon = False
        
    def show_items(self):
        pass
        
    def carry_item(self, item):
        if len(self.items) < INVENTORY_SIZE:
            self.items.append(item)
            return True
        else:
            return False
    
    def drink(self, potion):
        add = min(potion.hp * self.max_hp, self.max_hp - self.hp)
        self.hp += add
        self.items.remove(potion)
        
    def drop(self, item):
        """ Drops items from the inventory. Chests are preferred.
            Otherwise items are dropped to the ground nearby.
        """
        
        chests = []
        for direction in DIRECTIONS.values():
            x, y = self.new_pos(direction)
            if world.is_occupied(x, y) and isinstance(world.map[x][y], Chest):
                chests.append(world.map[x][y])
                break
        
        if item == self.weapon:
            self.weapon = False
                
        if len(chests):
            chests[0].items.append(item)
            self.items.remove(item)
        else:
            for direction in DIRECTIONS.values():
                x, y = self.new_pos(direction)
                if not world.is_occupied(x, y):
                    item.x, item.y = x, y
                    item.occupy()
                    self.items.remove(item)
                    break
    
    def draw_weapon(self, item):
        self.weapon = item
    
    def open(self):
        """ Checks if anything openable is around and if true
            calls the open method of the object.
        """
        for direction in DIRECTIONS.values():
            x, y = self.new_pos(direction)
            # tuple of openable classes like doors etc.
            # NEEDS TO BE A TUPLE!
            possibles = (Chest)
            if world.is_occupied(x, y) and isinstance(world.map[x][y], possibles):
                world.map[x][y].open()
                return
            
    def pick(self, inventory = None, pos = ()):
        if not inventory:
            # checkout if anything pickable is around
            for direction in DIRECTIONS.values():
                x, y = self.new_pos(direction)
                if world.is_occupied(x, y):
                    # check if item
                    if isinstance(world.map[x][y], Item):
                        if self.carry_item(world.map[x][y]):
                            # remove item from map when picked up
                            world.map[x][y].remove()
                            return
        else:
            # if picked from chest inventory
            inventory.transact(pos, self)
            
class Enemy(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, CHR_ENEMY, hp)
        
    def act(self, character):
        choices = [0, 1]
        
        dist = self.distance(character)
        if dist == (0, 1) or dist == (1, 0):
            choices.append(2)
        choice = random.choice(choices)
        
        if choice == 1:
            # Moving
            while (True):
                goto = random.choice(DIRECTIONS.values())
                new_x, new_y = self.new_pos(goto)
                if not world.is_occupied(new_x, new_y):
                    self.move(goto)
                    break
        elif choice == 2:
            # Fighting back
            self.attack(character)

class Wizard(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, CHR_WIZARD, hp)

    def cast_spell(self, name, target):
        """Cast a spell on the given target."""
        if name == 'remove':
            self._cast_remove(target)
        elif name == 'hp-stealer':
            self._cast_hp_stealer(target)
        else:
            print "The wizard does not know the spell '{0}' yet.".format(name)

    def _cast_remove(self, enemy):
        dist = self.distance(enemy)
        if dist == (0, 1) or dist == (1, 0):
            enemy.remove()

    def _cast_hp_stealer(self, enemy):
        dist = self.distance(enemy)
        if dist == (0, 3) or dist == (3, 0):
            enemy.harm(3)
            self.hp += 3
