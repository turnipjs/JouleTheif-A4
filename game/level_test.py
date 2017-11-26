import game
import creatures
import pygame
import json
import levels

class LevelExample(levels.Level):
	def on_setup(self):
		self.load_level("../sample-level.png")
		self.create_player((300,300))