import game
import pygame

class SimpleImageEntity(game.Entity):
	def __init__(self, path=None, **k):
		game.Entity.__init__(self, **k)
		self.image = pygame.image.load(path).convert()
		self.image.set_colorkey((255,0,255))
		self.size = self.image.get_size()

	def draw(self, dt):
		self.level.surf.blit(self.image, self.pos)