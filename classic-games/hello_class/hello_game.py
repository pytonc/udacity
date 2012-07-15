#!/usr/bin/env python
# hello_game.py
# This file implements the main class that will control a Gameplay

from classes import *
from ui_pygame import *
from ui_txt import *
import pickle

class HelloGame(object):
	def __init__(self, config, frontend = "txt"):
		self.config = config

		map_width = config.getint("WordMap", "width")
		map_height = config.getint("WordMap", "height")

		# Initialize game Frontend
		if frontend == "sdl":
			print "Initializing PyGame / SDL frontend"
			if map_width > 0 and map_height > 0:
				self.ui = SDLUserInterface(self, maps_width, map_height)
			else:
				self.ui = SDLUserInterface(self)
		elif frontend == "txt":
			print "Initializing ASCII frontend"
			if map_width > 0 and map_height > 0:
				self.ui = TXTUserInterface(self, map_width, map_height)
			else:
				self.ui = TXTUserInterface(self)
		else:
			print "Unknown UI frontend " + frontend + ". Aborting!"
			sys.exit(2)

		savefile = config.get("GameHandler", "savefile")
		if savefile != None:
			self.savefile = savefile


	def start_game(self, level):
		student_data = self.config.get(level, 'student').split(',')
		self.ui.add_student(student_data)

		engineer_data = self.config.get(level, 'engineer').split(',')
		self.ui.add_engineer(engineer_data)

		bugs_data = self.config.get(level, 'bug').split(';')
		for el in bugs_data:
			self.ui.add_enemy(el.split(','))

		self.ui.set_statusbar_character(self.ui.get_student())

		self.ui.draw_map()
		self.ui.mainloop()

	def save_game(self):
		outfile = open(self.savefile, "wb")
		pickle.dump(self.ui, outfile)
		outfile.close()

	def load_saved_game(self):
		pass
		# XXX
		#infile = open(self.savefile, "r")
		#tmpui = pickle.load(infile)
		#tmpui.draw_map()
		#self.ui = tmpui
