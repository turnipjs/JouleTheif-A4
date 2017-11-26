import pygame, json, sys

if len(sys.argv)!=2:
	print("Usage: python3 recttool.py some_level.jpg")
	sys.exit(1)

filename = sys.argv[1]

pygame.init()

image = pygame.image.load(filename)
try:
	with open(filename+".rects", 'r') as fd:
		rects = json.load(fd)["rects"]
except (IOError, json.decoder.JSONDecodeError):
	rects = []

screen = pygame.display.set_mode((1700, 900))

def save():
	with open(filename+".rects", 'w') as fd:
		json.dump({"rects":rects}, fd)

origin=None
offset=[0,0]

run=True
while run:
	screen.fill((0,0,0))
	screen.blit(image, offset)
	for r in rects:
		pygame.draw.rect(screen, (255,0,0), pygame.Rect(*r).move(offset), 1)
	if origin:
		end = pygame.mouse.get_pos()
		sz = [end[0]-origin[0]-offset[0], end[1]-origin[1]-offset[1]]
		pygame.draw.rect(screen, (0,255,0), pygame.Rect(*origin, *sz).move(offset), 1)
	pygame.display.flip()
	for e in pygame.event.get():
		if e.type==pygame.QUIT:
			run=False
		if e.type==pygame.KEYDOWN:
			if e.key==pygame.K_q:
				run=False
			if e.key==pygame.K_s:
				save()
		if e.type==pygame.MOUSEBUTTONDOWN:
			print(e.button)
			if e.button==1:
				p=pygame.mouse.get_pos()
				origin=[p[0]-offset[0], p[1]-offset[1]]
			if e.button==3:
				m=list(pygame.mouse.get_pos())
				m[0]-=offset[0]
				m[1]-=offset[1]
				print(m, rects)
				p=[r for r in rects if pygame.Rect(*r).collidepoint(m)]
				rects.remove(p[0]) if p else None
		if e.type==pygame.MOUSEBUTTONUP:
			if e.button==1:
				end = pygame.mouse.get_pos()
				sz = [end[0]-origin[0]-offset[0], end[1]-origin[1]-offset[1]]
				rects.append((*origin, *sz))
				origin=None
		if e.type==pygame.MOUSEMOTION:
			if e.buttons[1]:
				offset[0]+=e.rel[0]
				offset[1]+=e.rel[1]

save()