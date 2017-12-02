import game
import pygame

class SimpleImageEntity(game.Entity):
	def __init__(self, path=None, **k):
		game.Entity.__init__(self, **k)
		if path:
			self.image = pygame.image.load(path).convert()
		else:
			self.image = Surface((0, 0))
		self.image.set_colorkey((255, 0, 255))
		self.size = self.image.get_size()

	def draw(self, dt):
		self.level.surf.blit(self.image, self.pos)

class ParallaxScroller(game.Entity):
	def __init__(self, path=None, image=None, factor=0.75, **k):
		game.Entity.__init__(self, **k)
		if path:
			self.image = pygame.transform.scale2x(pygame.image.load(path).convert_alpha())
		else:
			self.image = image
		if self.image is None:
			self.image = Surface((0, 0))
		self.image.set_colorkey((255, 0, 255))
		self.size = self.image.get_size()
		self.factor = factor

	def draw(self, dt):
		num_required = 3+(self.level.surf.get_size()[0]//self.image.get_width())
		p_offset = self.level.scroll_pos[0] * -self.factor
		for idx in range(num_required + 2):
			self.level.surf.blit(self.image, (p_offset + (self.x + self.image.get_width() * (idx - 1)), self.y))
