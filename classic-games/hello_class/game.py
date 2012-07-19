#!/usr/bin/env python
# game.py - simple game to demonstrate classes and objects
import pygame
from pygame.locals import *

import sys

from classes import *

if __name__ == '__main__':

    # initializing some entities
    student = Player(10, 10, 100)
    engineer = Wizard(25, 14, 100)
    enemies = [
        Enemy(12, 10, 100),
        Enemy(10, 12, 100)
     ]
    Chest(7, 9, [
        Sword('Sword', 5),
        Potion(),
        Item('Spoon')
    ])
    Sword('Knife', 2, x = 8, y = 10)
    Item('Screw', 20, 6)

    student.items = [
        Potion()
    ]
    
    inventory = MyInventory(student)
    statustext.set_character(student)
    help = Help()
    
    while True:
        screen.fill((255,255,255))
        screen.blit(background, (0, 0 + STATUS_HEIGHT))
    
        # gets all entities that are set on world map
        entities = [entity for row in world.map for entity in row if entity]
        
        for e in entities:
            if e.sprite:
                screen.blit(e.sprite, (e.x * DIST, e.y * DIST + STATUS_HEIGHT))
        
        statustext.draw()
        inventory.draw()
        chest_inventory.draw()
        help.draw()
            
        for event in pygame.event.get():
            # QUIT
            if event.type == QUIT:
                sys.exit(0)
                
            elif event.type == KEYDOWN:
                # move
                if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                    student.move(DIRECTIONS[event.key])
                    for enemy in enemies:
                        enemy.act(student)
                # attack
                elif event.key == K_a:
                    student.attack()
                    for enemy in enemies:
                        enemy.act(student)
                # show help
                elif event.key == K_h:
                    help.show(not help.visible)
                # show items
                elif event.key == K_i:
                    inventory.show(not inventory.visible)
                # open chest
                elif event.key == K_o:
                    student.open()
                    inventory.show(chest_inventory.visible)
                # pick item
                elif event.key == K_p:
                        student.pick()
                # QUIT
                elif event.key == K_ESCAPE:
                    sys.exit(0)
                    
            elif event.type == MOUSEBUTTONDOWN:
                # right mouse click
                if event.button == 3:
                    # item menus
                    if inventory.visible:
                        inventory.show_menu(event.pos)
                    # pciking item
                    if chest_inventory.visible:
                        student.pick(chest_inventory, event.pos)
                # left mouse click
                elif event.button == 1:
                    inventory.select_item(event.pos)
                
        pygame.display.update()
