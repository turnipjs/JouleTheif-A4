import game
import creatures
import pygame
import json
import levels

class LevelExample(levels.Level):
	def on_setup(self):
		self.load_level("asset/mongolevel.png")
		self.create_player((300,300))
		self.add_entity(creatures.SimpleImageEntity(path="asset/redsquare.png", x=200, y=740)).on_collided_with=lambda o:self.game.set_state(LevelExample2())
		self.enable_scrolling()

class LevelExample2(levels.Level):
	def on_setup(self):
		self.load_level("asset/sample-level.png")
		self.create_player((200,200))
		self.add_entity(creatures.SimpleImageEntity(path="asset/redsquare.png", x=400, y=400)).on_collided_with=lambda o:self.game.set_state(LevelExample())