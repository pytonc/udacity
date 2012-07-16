#!/usr/bin/env python
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
    tilesImg = []                            #List of images used in map
    
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
        for x in range(7):
            imgTemp = Image.open("map.png")                     # open image
            imgTemp = imgTemp.crop((x*16,0,x*16+16,16))         # crop it
            self.tilesImg.append(ImageTk.PhotoImage(imgTemp))         # add to list, a format of image usable by canvas 
       
    #--- PRINT STATUS TEXT ---
    def printText(self, inputText):
        self.mapCanvas.delete(ALL)
        self.paintMap(None)
        self.mapCanvas.create_text(10, world.height*16+10, anchor=W, font="Arial", text=inputText)
        
    #--- PAINT, REFRESH MAP ---
    def paintMap(self, event):  #based on object "world" - world map that contains map objects, defined in classes.py
        self.mapCanvas.delete(ALL)  #delete previous objects
        #instruction text
        self.mapCanvas.create_text(10, world.height*16+30, anchor=W, font="Arial", text="Moving: [u] [d] [l] [r] <Up> <Down> <Left> <Right>  |  Attack: [a]  |  GPS: [g]")
        
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
                    else:   # for X, when bugs die
                        self.mapCanvas.create_image(x*16, (world.height - 1 - y)*16, image = self.tilesImg[6], anchor = NW)
                        
                except:
                    pass
#Create objects
student = Player(10, 10, 100)
engineer = Wizard(35, 14, 100)
bug1 = Enemy(12, 10, 100)
bug2 = Enemy(11, 11, 100)
    
statusbar.set_character(student)      
                    
#=============================================
# COMMANDS
#=============================================
def move_enemies():
    bug1.act(student, DIRECTIONS)
    bug2.act(student, DIRECTIONS)

def move_student_left(event):
    student.move("left")
    move_enemies()
    mainMapGUI.paintMap(None) 

def move_student_right(event):
    student.move("right")
    move_enemies()
    mainMapGUI.paintMap(None) 

def move_student_up(event):
    student.move("up")
    move_enemies()
    mainMapGUI.paintMap(None) 

def move_student_down(event):
    student.move("down")
    move_enemies()
    mainMapGUI.paintMap(None) 
    
    
def attack(event):
    enemies = student.get_alive_enemies(1)
    if enemies:
        student.attack(enemies[0])
        enemies[0].act(student, DIRECTIONS)
    tempStr = "Bug now has: " + str(bug1.hp) + " hp left"
    mainMapGUI.printText(tempStr)

def gps(event):
    tempStr = "Your location: " + str(student.x) + ", " + str(student.y) + "   Bug location: " + str(bug1.x) + ", " + str(bug1.y)
    mainMapGUI.printText(tempStr)


#=============================================
# MAIN PROGRAM
#=============================================

if __name__ == '__main__':

        
    mainMapGUI = mapGUI()                           #Create instance of GUI map class
    
    ### KEY BIND ###
    rootTk.bind('l', move_student_left)             # Moving Left
    rootTk.bind('<Left>', move_student_left)
    rootTk.bind('r', move_student_right)             # Moving Right
    rootTk.bind('<Right>', move_student_right)
    rootTk.bind('u', move_student_up)               # up
    rootTk.bind('<Up>', move_student_up)
    rootTk.bind('d', move_student_down)             # down
    rootTk.bind('<Down>', move_student_down)
    rootTk.bind('a', attack)
    rootTk.bind('g', gps)
    
    mainMapGUI.paintMap(None)
    rootTk.mainloop()  

#EOF