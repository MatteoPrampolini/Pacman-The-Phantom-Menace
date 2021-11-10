import time
import pygame
import os
import sys
from enum import Enum
import numpy as np
import graphics as gp
from entities import Pacman, RedGhost 
class Actions():
	UP =  [1,0,0,0]
	DOWN = [0,1,0,0]
	LEFT = [0,0,1,0]
	RIGHT = [0,0,0,1]
class ENTITIES(Enum):
	PACMAN = 0
	RED = 1
	PINK = 2
	CYAN = 3
	YELLOW = 4
pygame.font.init()	# text init
pygame.mixer.init()	 # sound init

WIDTH, HEIGHT = 448, 576
pygame.display.set_caption("Pacman")

#game settings
FPS = 60
VEL = 3

class Game():
	def __init__(self, w=WIDTH, h=HEIGHT):
		self.w=w
		self.h=h
		self.clock = pygame.time.Clock()
		self.graphics = gp.PacGraphic(w,h) #questa classe gestisce tutto cio' che e' grafico.
		#initialize entities
		self.entities = list()
		#pacman=Pacman(os.path.join('Assets', 'pac-tmp.png'),x=int(WIDTH/2),y=int(HEIGHT/2)-70,name="pacman")
		pacman=Pacman(os.path.join('Assets', 'pac-tmp.png'),name="pacman")
		x,y=self.graphics.grid_to_window(row=22,col=13)
		pacman.default_x=x
		pacman.default_y=y+6
		pacman.set_rect(pacman.default_x,pacman.default_y,26,26)
		self.entities.append(pacman)
		red=RedGhost(os.path.join('Assets', 'red-tmp.png'),name="blinky")
		x,y=self.graphics.grid_to_window(row=10,col=13)
		red.default_x=x
		red.default_y=y+6
		red.set_rect(red.default_x,red.default_y,26,26)
		self.entities.append(red)
		self.graphics.get_entities(self.entities)
		self.reset()
		
	def reset(self):
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.graphics.reset()
		self.graphics.get_grid(self.grid)
		self.debug=False
		self.is_running=True
		self.is_game_over=False
		
	def handle_entity_movement(self,entity,keys_pressed):
		rect= entity.rect
		
		#IF PACMAN
		if entity.name=="pacman":
			left_key=pygame.K_a
			right_key=pygame.K_d
			up_key=pygame.K_w
			down_key=pygame.K_s
		#IF BLINKY (RED)
		else: 
			left_key=pygame.K_LEFT
			right_key=pygame.K_RIGHT
			up_key=pygame.K_UP
			down_key=pygame.K_DOWN
			
		#MOVE
		if keys_pressed[left_key] and rect.x - VEL > 0:  # LEFT
			if self.can_move(Actions.LEFT,entity):
				rect.x -= VEL
		if keys_pressed[right_key] and rect.x + VEL + rect.width < WIDTH:	# RIGHT
			if self.can_move(Actions.RIGHT,entity):
				rect.x += VEL
		if keys_pressed[up_key] and rect.y - VEL > 0:	# UP
			if self.can_move(Actions.UP,entity):
				rect.y -= VEL
		if keys_pressed[down_key] and rect.y + VEL + rect.height < HEIGHT:	 # DOWN
			if self.can_move(Actions.DOWN,entity):
				rect.y += VEL
		if entity.name=="pacman":
			x,y=entity.window_to_grid()
			if self.grid[y][x]==1:
				self.grid[y][x]=0

	#wx,wy mi servono per allineare bene le sprites alla griglia, perché le collisioni della grid sono spartane
	def can_move(self,action,entity):
		x,y=entity.window_to_grid()
		if action == Actions.UP and self.grid[y-1,x]==2:
			wx,wy=self.graphics.grid_to_window(y+1,x)
			y=entity.rect.y+entity.rect.height
			if y > wy :
				return True
			return False
		if action == Actions.DOWN and self.grid[y+1,x]==2:
			wx,wy=self.graphics.grid_to_window(y+1,x)
			y=entity.rect.y+entity.rect.height
			if y < wy :
				return True
			return False

		if action == Actions.LEFT and self.grid[y,x-1]==2:
			wx,wy=self.graphics.grid_to_window(y,x-1)
			x=entity.rect.x-entity.rect.width/2
			if x > wx :
				return True
			return False
		if action == Actions.RIGHT and self.grid[y,x+1]==2:
			wx,wy=self.graphics.grid_to_window(y,x+1)
			x=entity.rect.x+entity.rect.width
			if x < wx :
				return True
			return False
		return True
		
		
		
def main():

	game= Game()
	while True:
		check_for_events(game)
		if not game.is_running:
			continue
		keys_pressed = pygame.key.get_pressed()

		game.clock.tick(FPS)
		for entity in game.entities:
			game.handle_entity_movement(entity,keys_pressed)
		game.graphics.draw_window(game.debug)
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
if __name__ == "__main__":
	main()
