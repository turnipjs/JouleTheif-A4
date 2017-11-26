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

class ParralaxScroller(game.Entity):
	def __init__(self, path=None, image=None, factor=0.75, **k):
		game.Entity.__init__(self, **k)
		self.image=image
		if path:
			self.image = pygame.transform.scale2x(pygame.image.load(path).convert_alpha())
			self.image.set_colorkey((255,0,255))
		self.size = self.image.get_size()
		self.factor=factor

	def draw(self, dt):
		num_required = 3+(self.level.surf.get_size()[0]//self.image.get_width())
		p_offset=self.level.scroll_pos[0]*-self.factor
		for idx in range(num_required+2):
			self.level.surf.blit(self.image, (p_offset+(self.x+self.image.get_width()*(idx-1)), self.y))