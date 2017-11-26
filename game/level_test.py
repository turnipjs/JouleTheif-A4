import game
import creatures
import pygame
import json
import levels

class LevelExample(levels.Level):
	def on_setup(self):
		self.load_level("test_level.png")
		self.create_player((300,300))
		self.add_entity(creatures.SimpleImageEntity(path="redsquare.png", x=1320, y=740)).on_collided_with=lambda o:self.game.set_state(LevelExample2())

class LevelExample2(levels.Level):
	def on_setup(self):
		self.load_level("../sample-level.png")
		self.create_player((200,200))