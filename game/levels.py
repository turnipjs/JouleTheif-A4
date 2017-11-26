import game
import creatures
import json
import pygame

class Level(game.GameplayState):
	def load_level(self, path):
		self.add_entity(creatures.SimpleImageEntity(path=path, is_solid=False, obey_gravity=False, can_collide=False))
		with open(path+".rects", 'r') as fd:
			for rect in json.load(fd)["rects"]:
				if rect[2] < 0:
					rect[0] += rect[2]
					rect[2] *= -1
				if rect[3] < 0:
					rect[1] += rect[3]
					rect[3] *= -1
				self.add_entity(game.Entity(x=rect[0], y=rect[1], size_x=rect[2], size_y=rect[3], obey_gravity=False, can_collide=False))
	
	def create_player(self, start):
		self.player=self.add_entity("player", creatures.SimpleImageEntity(path="Kyou.png", x=start[0], y=start[1]))
		return self.player

	def update(self, dt):
		game.GameplayState.update(self, dt)
		self.do_player_movement(dt)

	def do_player_movement(self, dt, move_accel_speed=3000, move_cap=300, jump_power=400):
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
