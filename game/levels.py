import game

class Level(game.GameplayState):
    def __init__(self, lvName, start):
        self.lvName = lvName
        self.start = start

    def on_setup(self):
		self.add_entity(creatures.SimpleImageEntity(path=self.lvName, is_solid=False, obey_gravity=False, can_collide=False))
		with open(level_path+".rects", 'r') as fd:
			for rect in json.load(fd)["rects"]:
				if rect[2] < 0:
					rect[0] += rect[2]
					rect[2] *= -1
				if rect[3] < 0:
					rect[1] += rect[3]
					rect[3] *= -1
				self.add_entity(game.Entity(x=rect[0], y=rect[1], size_x=rect[2], size_y=rect[3], obey_gravity=False, can_collide=False))
		self.player = self.add_entity("player", creatures.SimpleImageEntity(path="Kyou.png", x=self.start[0], y=self.start[1]))

	def update(self, dt):
		game.GameplayState.update(self, dt)

		move_accel_speed=3000
		move_cap=300
		jump_power=400

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
