###!/usr/bin/env python
""""
[GFX functionality with Tkinter] by 58982/ken-price
VERSION 2
Project:         udacity/classic-games
Date:            7/16/2012
Dependencies:    "classes.py", Tkinter, PIL,
Description:     By Ken Price; First entry for Udacity contest ending July 23rd. A class, mapGUI, that displays
                 a graphical map of the world.

                Intended as possible replaement for game.py
"""
from Tkinter import *               # For GUI
from PIL import Image, ImageTk      # For Image conversion
from classes import *               # game classes

rootTk = Tk()               # Tkinter root object

DIRECTIONS = {
    "r": "right",
    "l": "left",
    "d": "down",
    "u": "up"
}

#=============================================
# MAP GUI CLASS
#=============================================
class mapGUI(Frame):  #based on Frame from Tkinter
    #--- VARIABLES ---
    mapCanvas = Canvas(rootTk, width=world.width*16, height=world.height*16) #Canvas for gfx map
    tilesImg = []
                            #List of images used in map

    #--- CONSTRUCTOR ---
    def __init__(self):
        Frame.__init__(self)    #calling super-class constructor
        self.parent = rootTk            #save parent reference

        self.initImages()           #initialize images
        self.initUI()               #initialize UI items

        rootTk.geometry(str(world.width*16)+"x"+str(world.height*16+100)+"+300+300")        #width/height/x/y

    #--- INITIALIZE UI ---
    def initUI(self):
        self.parent.title("Map GUI")
        self.pack(fill=BOTH, expand=1)               # 'pack' or place frame (window)
        self.mapCanvas.pack(fill=BOTH, expand=1)    # place canvas

    #--- LOAD IMAGES ---
    def initImages(self):
        # map.png has 16x16 pixel tiles placed side-by-side. the following loop will take each of these tiles
        # and store them in the tilesImg list
        steps = 14
        map_to_use = "map.png"
        for y in range(2):
            for x in range(steps):
                imgTemp = Image.open(map_to_use)
                imgTemp = imgTemp.crop((x*16,0,x*16+16,16))
                self.tilesImg.append(ImageTk.PhotoImage(imgTemp))

            map_to_use = "map2.png"
            steps = 3


    #--- PRINT STATUS TEXT ---
    def printText(self, inputText):
        self.mapCanvas.delete(ALL)
        self.paintMap(None)
        self.mapCanvas.create_text(10, world.height*16+10, anchor=W, font="Arial", text=inputText)

    #--- PAINT, REFRESH MAP ---
    def paintMap(self, event):  #based on object "world" - world map that contains map objects, defined in classes.py
        self.mapCanvas.delete(ALL)  #delete previous objects
        #instruction text
        self.mapCanvas.create_text(10, world.height*16+30, anchor=W, font="Arial", text="Moving: <Up> <Down> <Left> <Right>  |  Attack: [a]  |  GPS: [g]  |  HP: [h]")

        for x in range(0, world.width):
            for y in range(0, world.height):    #loop through each cell
                cell = world.map[x][y]          #temporary placeholder of object in cell

                try:
                    if cell is None:            #empty cell, blank image (index 0)
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[0], anchor = NW)
                    elif cell.image == 'S':   #
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[2], anchor = NW)
                    elif cell.image == 'W':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[3], anchor = NW)
                    elif cell.image == 'A':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[4], anchor = NW)
                    elif cell.image == 'B':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[5], anchor = NW)
                    elif cell.image == 'F':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[7], anchor = NW)
                    elif cell.image == 'T':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[8], anchor = NW)
                    elif cell.image == 'L':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[9], anchor = NW)
                    elif cell.image == 'G':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[10], anchor = NW)
                    elif cell.image == 'R':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[11], anchor = NW)
                    elif cell.image == 'GT':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[12], anchor = NW)
                    elif cell.image == 'WL':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[13], anchor = NW)
                    elif cell.image == 'TLR':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[15], anchor = NW)
                    elif cell.image == 'TLG':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[14], anchor = NW)
                    elif cell.image == 'BF':
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[16], anchor = NW)
                    else:   # for X, when bugs die
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[6], anchor = NW)

                except:
                    pass
#Create objects
student = Player(12, 12)
engineer1 = Wizard(35, 13)
engineer2 = Wizard(56,21)
bug1 = Enemy(55,12)
bug2 = Enemy(20, 15)

fountain1 = Fountains((world.width/8)-4, (world.height/2)-2)
fountain2 = Fountains((world.width/8)-3, (world.height/2)+2)
trees = Tree(random.randint(1,world.width-1), random.randint(1,world.height-1), 6)
leafs = Leaf_Tree( random.randint(1,world.width-1), random.randint(1,world.height-1), 6)
green_car = Car(random.randint(1,world.width-1), random.randint(1,world.height-1), 'G')
red_car = Car(random.randint(1,world.width-1), random.randint(1,world.height-1), 'R')
gates = Gate((world.width/6), (world.height/2))
wall = Wall((world.width/6), (world.height/2 + 1))
tr_light = Traffic_Light((world.width/6), (world.height/2)-1)
butterfly = Butterfly(20,17)



statusbar.set_character(student)

#=============================================
# COMMANDS
#=============================================
def move_enemies():
    bug1.act(student, DIRECTIONS)
    bug2.act(engineer2, DIRECTIONS)

def move_others():
    gates.open_close(student)
    engineer1.act_Wizard(bug2, DIRECTIONS)
    engineer2.act_Wizard(bug2, DIRECTIONS)
    fountain1.heal(student)
    fountain2.heal(student)
    green_car.walk(DIRECTIONS)
    red_car.walk(DIRECTIONS)
    tr_light.work(student)
    butterfly.fly(student, DIRECTIONS)

def move_student(event):
    direction = event.keysym.lower()
    student.move(direction)
    move_enemies()
    move_others()
    mainMapGUI.paintMap(None)

def student_sleep(event):
    student.stay()
    move_enemies()
    move_others()
    mainMapGUI.paintMap(None)

def attack(event):
    enemies = student.get_alive_enemies(1)
    if enemies:
        student.attack(enemies[0])
        enemies[0].act(student, DIRECTIONS)
    else:
        tempStr = "There is no any enemy around."
    tempStr = "Bug1 now has: " + str(bug1.hp) + " hp left" + "  and Bug2 now has: " + str(bug2.hp) + " hp left"
    mainMapGUI.printText(tempStr)

def gps(event):
    tempStr = "Your location: " + str(student.x) + ", " + str(student.y) + "   Bug1 location: " + str(bug1.x) + ", " + str(bug1.y) + "   Bug2 location:  " + str(bug2.x) + ", " + str(bug2.y)
    mainMapGUI.printText(tempStr)

def hp_checker(event):
    tempStr = "You have " + str(student.hp) + " hp left"
    mainMapGUI.printText(tempStr)



#=============================================
# MAIN PROGRAM
#=============================================

if __name__ == '__main__':


    mainMapGUI = mapGUI()                           #Create instance of GUI map class

    ### KEY BIND ###

    rootTk.bind('<Left>', move_student)
    rootTk.bind('<Right>', move_student)
    rootTk.bind('<Up>', move_student)
    rootTk.bind('<Down>', move_student)
    rootTk.bind('a', attack)
    rootTk.bind('g', gps)
    rootTk.bind('h', hp_checker)
    rootTk.bind('s', student_sleep)

    mainMapGUI.paintMap(None)
    rootTk.mainloop()

#EOF