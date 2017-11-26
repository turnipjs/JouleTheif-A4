import game
import entities
import json
import pygame

class GameplayState(game.GameState):
	def __init__(self):
		game.GameState.__init__(self)
		self.entities_dict = {}
		self._id=0
		self.scroll=False
		self.scroll_pos=[0,0]
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
		self.surf.fill((0,0,100))
		self.on_update(dt)
		for e in self.entities:
			e.update(dt)
		pos = (0,0)
		if self.scroll:
			ss=self.game.screen.get_size()
			ws=self.surf.get_size()
			ps=self.player.size
			pos = [
				-self.player.x - ps[0] + (ss[0]/2),
				-self.player.y - ps[1] + (ss[1]/2)
			]
			if pos[0]>0:
				pos[0]=0
			if pos[1]>0:
				pos[1]=0
			if pos[0]<(ss[0]-ws[0]):
				pos[0]=ss[0]-ws[0]
			if pos[1]<(ss[1]-ws[1]):
				pos[1]=ss[1]-ws[1]

		self.scroll_pos=pos

		self.game.screen.blit(self.surf, pos)

	def on_update(self, dt):
		pass

	def handle_events(self, events):
		pass

	def get_gravity(self):
		return 600

class Level(GameplayState):
	def load_level(self, path):
		self.map_ent = self.add_entity(entities.SimpleImageEntity(path=path, is_solid=False, obey_gravity=False, can_collide=False))
		with open(path+".rects", 'r') as fd:
			for rect in json.load(fd)["rects"]:
				if rect[2] < 0:
					rect[0] += rect[2]
					rect[2] *= -1
				if rect[3] < 0:
					rect[1] += rect[3]
					rect[3] *= -1
				self.add_entity(game.Entity(x=rect[0], y=rect[1], size_x=rect[2], size_y=rect[3], obey_gravity=False, can_collide=False))
		self.surf = pygame.Surface(self.map_ent.size)
	
	def create_player(self, start):
		self.player=self.add_entity("player", entities.SimpleImageEntity(path="asset/Kyou.png", x=start[0], y=start[1]))
		return self.player

	def update(self, dt):
		GameplayState.update(self, dt)
		self.do_player_movement(dt)

	def do_player_movement(self, dt, move_accel_speed=3000, move_cap=300, jump_power=800):
		p = pygame.key.get_pressed()
		moved = False
		if p[pygame.K_a]:
			self.player.vel_x-=move_accel_speed*dt
			moved = True
		if p[pygame.K_d]:
			self.player.vel_x+=move_accel_speed*dt
			moved = True
		if not moved:
			self.player.vel_x-=move_accel_speed*dt*(1 if self.player.vel_x>0 else -1)
			if abs(self.player.vel_x)<=move_accel_speed*dt:
				self.player.vel_x=0

		if self.player.vel_x>move_cap: self.player.vel_x=move_cap
		if self.player.vel_x<-move_cap: self.player.vel_x=-move_cap
		if p[pygame.K_w] and self.player.on_ground:
			self.player.vel_y=-jump_power

	def enable_scrolling(self):
		self.scroll=True
