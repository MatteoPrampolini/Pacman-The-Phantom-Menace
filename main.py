import time
import pygame
import os
import sys
from enum import Enum
import numpy as np
import graphics as gp
from entities import Pacman, RedGhost, PinkGhost
import heapq
class Actions():
	UP 	 = [1,0,0,0,0]
	DOWN = [0,1,0,0,0]
	LEFT = [0,0,1,0,0]
	RIGHT= [0,0,0,1,0]
	HALT = [0,0,0,0,1]
class ENTITIES(Enum):
	PACMAN = 0
	RED = 1
	PINK = 2
	CYAN = 3
	GOLD = 4
pygame.font.init()	# text init
pygame.mixer.init()	 # sound init

WIDTH, HEIGHT = 448, 576
pygame.display.set_caption("Pacman")
#game settings
FPS = 60

class Game():
	def __init__(self, w=WIDTH, h=HEIGHT):
		self.w=w
		self.h=h
		self.frame_iteration = 0
		self.game_started= False
		self.graphics = gp.PacGraphic(w,h) #questa classe gestisce tutto cio' che e' grafico.
		#0=clear_path,2=wall,1=coin,3=invalid
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		#initialize entities
		self.clock = pygame.time.Clock()
		self.entities = list()
		self.init_entities()
		self.graphics.get_entities(self.entities)
		self.reset()
		
	def reset(self):
		self.frame_iteration = 0
		#0=clear path,1=wall,2=coin path,3=invalid
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		
		self.graphics.reset()
		self.graphics.get_grid(self.grid)
		self.debug=False
		self.is_running=True
		self.is_game_over=False
	
	def init_entities(self):
		pacman=Pacman(os.path.join('Assets', 'pac-tmp.png'),name="pacman")
		x,y=self.graphics.grid_to_window(row=23,col=13)

		pacman.default_x=x
		pacman.default_y=y+48-6
		pacman.set_rect(pacman.default_x,pacman.default_y,26,26)
		self.entities.append(pacman)
		#RED
		red=RedGhost(os.path.join('Assets', 'red-tmp.png'),self.grid,name="blinky")
		x,y=self.graphics.grid_to_window(row=11,col=13)
		red.default_x=x
		red.default_y=y+48-6
		red.set_rect(red.default_x,red.default_y,26,26)
		self.entities.append(red)
		#PINK
		# pink=PinkGhost(os.path.join('Assets', 'pink-tmp.png'),self.grid,name="pinky")
		# x,y=self.graphics.grid_to_window(row=11,col=13)
		# pink.default_x=x
		# pink.default_y=y+48-6
		# pink.set_rect(pink.default_x,pink.default_y,26,26)
		# self.entities.append(pink)
	
	
	def move_entity(self,entity,action):
		rect=entity.rect
		VEL=entity.VEL
		if action==Actions.LEFT and rect.x - VEL > 0:  # LEFT
			if self.can_move(Actions.LEFT,entity):
				rect.x -= VEL
				
		if action==Actions.RIGHT and rect.x + VEL + rect.width < WIDTH:	# RIGHT
			if self.can_move(Actions.RIGHT,entity):
				rect.x += VEL
		if action==Actions.UP and rect.y - VEL > 0:	# UP
			if self.can_move(Actions.UP,entity):
				rect.y -= VEL
		if action==Actions.DOWN and rect.y + VEL + rect.height < HEIGHT:	 # DOWN
			if self.can_move(Actions.DOWN,entity):
				rect.y += VEL
		if entity.name=="pacman":
			self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x]=0
		entity.pos_in_grid_x,entity.pos_in_grid_y=entity.window_to_grid()
	def coords_to_direction(self,x,y,dx,dy):
		#print(str(x)+">"+str(dx)+"="+str(x>dx))

		if x>dx:
			return Actions.LEFT
		if x<dx:
			return Actions.RIGHT
		if y<dy:
			return Actions.DOWN
		if y>dy:
			return Actions.UP
		
	#wx,wy mi servono per allineare bene le sprites alla griglia, perché le collisioni della grid sono spartane
	def can_move(self,action,entity):
		x,y=entity.window_to_grid()
		if action == Actions.UP and self.grid[y-1,x]==2:
			wx,wy=self.graphics.grid_to_window(y+1,x)
			y=entity.rect.y-entity.rect.height
			
			if y > wy :
				return True
			return False
		if action == Actions.DOWN and self.grid[y+1,x]==2:
			#wx,wy=self.graphics.grid_to_window(y+1,x)
			#y=entity.rect.y#+entity.rect.height
			#print(y,wy)
			#if y < wy :
			#	return True
			return False

		if action == Actions.LEFT and self.grid[y,x-1]==2:
			wx,wy=self.graphics.grid_to_window(y,x-1)
			x=entity.rect.x-entity.rect.width/2
			#print(x,wx)
			if x > wx :
				return True
			return False
		if action == Actions.RIGHT and self.grid[y,x+1]==2:
			#wx,wy=self.graphics.grid_to_window(y,x+1)
			#x=entity.rect.x#+entity.rect.width
			#if x < wx :
			#	return True
			return False
		return True 
	def play_step(self,action):
		if self.graphics.timer <2.5:
			#return #il timer lo abilito nella release, mentre sviluppo e' una perdita di tempo
			pass
		for entity in self.entities:
			entity.set_pos_in_grid()
			if entity.name != "pacman": #if ghost
				#LEGENDA: px=pacman_x,dx=destion_x (next step in path),ex=entity_x (ghost)
				px=self.entities[ENTITIES.PACMAN.value].pos_in_grid_x
				py=self.entities[ENTITIES.PACMAN.value].pos_in_grid_y
				dy,dx=entity.get_new_path(px,py) #where am i going to move
				ex=entity.pos_in_grid_x
				ey=entity.pos_in_grid_y
				#print("sono a: "+str(ey)+","+str(ex)+" e voglio andare a: "+str(dy)+","+str(dx))
				if dx==-1: #dovrebbe sempre trovare il path, questo if e' in caso l'universo si distrugga
					print("error")
					continue
					
				else: #if tutto bene
					action=self.coords_to_direction(ex,ey,dx,dy)
		
			self.move_entity(entity,action) 
				
			
		
		
def main():

	game= Game()
	while True:
		check_for_events(game)
		if not game.is_running:
			continue
		keys_pressed = pygame.key.get_pressed()
		game.clock.tick(FPS)
		game.frame_iteration+=1
		game.graphics.update_time(game.frame_iteration/FPS)
		game.graphics.draw_window(game.debug)
		action=check_keyboard() #questo ora e manuale, poi ci pensera' l'agents
		game.play_step(action) #ignorare il parametro per ora
		if game.is_game_over:
			game.reset()
def check_for_events(game):
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYUP: #keyup è meglio di keydown se vuoi premere il tasto una volta sola
				if event.key == pygame.K_p: #if P is pressed, toggle pause
					game.is_running=not game.is_running
				if event.key == pygame.K_m: #if M is pressed, toggle debug
					game.debug=not game.debug
				
				if event.key == pygame.K_r:
					game.reset()
					
				if 	event.key == pygame.K_y:
					win_x, win_y = pygame.mouse.get_pos()
					x=win_x//16
					y=(win_y- 48)//16
					if(x<28 and y<31):
						print("y:"+str(y)+",x:"+str(x)+"="+str(game.grid[y,x])+"\t"+str(win_y)+","+str(win_x))
					else:
						print("y:"+str(y)+",x:"+str(x)+"="+"fuori mappa")
def check_keyboard(): #debugging only
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_a]:
			return Actions.LEFT
		if keys_pressed[pygame.K_d]:
			return Actions.RIGHT
		if keys_pressed[pygame.K_w]:
			return Actions.UP
		if keys_pressed[pygame.K_s]:
			return Actions.DOWN
		else:
			return Actions.HALT
	
if __name__ == "__main__":
	main()
