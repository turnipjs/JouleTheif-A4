import pygame

game = None

class JouleThiefGame:
	def __init__(self, screen):
		self.screen = screen
		self.state = None

	def set_state(self, state):
		state.game = self
		self.state = state
		return self

	def mainloop(self):
		self.clock = pygame.time.Clock()
		while True:
			dt = self.clock.tick(60)
			if dt==0:
				continue
			dt=float(dt)/1000

			events = pygame.event.get()
			for event in events:
				if (event.type==pygame.KEYDOWN and event.key==pygame.K_q) or event.type==pygame.QUIT:
					1/0
			self.screen.fill((0,0,0))
			self.state.handle_events(events)
			self.state.update(dt)
			pygame.display.flip()

class GameState:
	def __init__(self):
		pass

	def update(self, dt):
		pass

	def handle_events(self, events):
		pass

class GameplayState(GameState):
	def __init__(self):
		GameState.__init__(self)
		self.entities_dict = {}
		self._id=0
		self.on_setup()

	@property
	def entities(self):
		return self.entities_dict.values()

	def entities_in_layer(self, layer):
		return {k:v for k,v in self.entities_dict.items() if v.layer==layer}

	def get_entity(self, name):
		return self.entities_dict[name]

	def has_entity(self, name):
		return name in self.entities_dict

	def add_entity(self, e_or_name, e=None):
		if e is None:
			e=e_or_name
			e_or_name=self._id
			self._id+=1
		self.entities_dict[e_or_name] = e
		e.level = self
		return e

	def update(self, dt):
		self.on_update(dt)
		for e in self.entities:
			e.update(dt)

	def on_update(self, dt):
		pass

	def handle_events(self, events):
		pass

	def get_gravity(self):
		return 600

class Entity:
	def __init__(self, x=0, y=0, size_x=0, size_y=0, vel_x=0, vel_y=0, layer=0, is_solid=True, can_collide=True, obey_gravity=True):
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.layer = layer
		self.is_solid = is_solid
		self.can_collide = can_collide
		self.obey_gravity = obey_gravity
		self.x, self.y, self.size_x, self.size_y = x, y, size_x, size_y
		self.level = None

	@property
	def pos(self):
		return (self.x, self.y)

	@pos.setter
	def pos(self, v):
		(self.x, self.y) = v

	@property
	def vel(self):
		return (self.vel_y, self.vel_y)

	@vel.setter
	def vel(self, v):
		self.vel_y, self.vel_y = v

	@property
	def size(self):
		return (self.size_x, self.size_y)

	@size.setter
	def size(self, v):
		self.size_x, self.size_y = v

	def get_rect(self):
		return pygame.Rect(self.pos, self.size)

	def update(self, dt):
		if self.obey_gravity:
			self.vel_y+=dt*self.level.get_gravity()

		self.x+=self.vel_x*dt
		if self.can_collide:
			new_rect=self.get_rect()
			platforms = [e.get_rect() for e in self.level.entities_in_layer(self.layer).values() if e.is_solid and e is not self]
			collided = False
			for p in platforms:
				if p.colliderect(new_rect):
					if self.vel_x>0:
						new_rect.right = p.left
						collided=True
					else:
						new_rect.left = p.right
						collided=True
			if collided:
				self.pos = new_rect.topleft


		self.y+=self.vel_y*dt
		if self.can_collide:
			new_rect = self.get_rect()
			collided = False
			self.on_ground = False
			for p in platforms:
				if p.colliderect(new_rect):
					if self.vel_y>0:
						new_rect.bottom = p.top
						collided=True
						self.on_ground=True
					else:
						new_rect.top = p.bottom
						collided=True
			if collided:
				self.pos = new_rect.topleft

		self.draw(dt)

	def draw(self, dt):
		pygame.draw.rect(self.level.game.screen, (255,0,0), self.get_rect(), 2)