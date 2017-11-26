import game
import creatures
import pygame
import json

class LevelExample(game.GameplayState):
	def on_setup(self):
		self.add_entity(creatures.SimpleImageEntity(path="something.gif", y=500, obey_gravity=False))
		self.add_entity(creatures.SimpleImageEntity(path="test_level.png", is_solid=False, obey_gravity=False, can_collide=False))
		with open("test_level.png.rects", 'r') as fd:
			for rect in json.load(fd)["rects"]:
				print(rect)
				if rect[2]<0:
					rect[0]+=rect[2]
					rect[2]*=-1
				if rect[3]<0:
					rect[1]+=rect[3]
					rect[3]*=-1
				print(rect)
				print()

				self.add_entity(game.Entity(x=rect[0], y=rect[1], size_x=rect[2], size_y=rect[3], obey_gravity=False, can_collide=False))
		self.player = self.add_entity("player", creatures.SimpleImageEntity(path="Kyou.png", x=300, y=300))

	def update(self, dt):
		game.GameplayState.update(self, dt)

		p = pygame.key.get_pressed()
		self.player.vel_x=0
		if p[pygame.K_a]:
			self.player.vel_x=-300
		elif p[pygame.K_d]:
			self.player.vel_x=300
		if p[pygame.K_w] and self.player.on_ground:
			self.player.vel_y=-400