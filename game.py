import time
import pygame
import os
import sys
from enum import Enum
import numpy as np
from entities import Pacman, RedGhost, PinkGhost, FACING
import graphics as gp
import heapq
class Actions(Enum):
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

 

class Game():
	def __init__(self, w=WIDTH, h=HEIGHT):
		self.w=w
		self.h=h
		self.frame_iteration = 0
		self.game_started= False
		self.graphics = gp.PacGraphic(w,h) #questa classe gestisce tutto cio' che e' grafico.
		#0=clear_path,2=wall,1=coin,3=invalid
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.memory=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],[2,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,2],[2,2,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,2,2],[3,3,3,3,3,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,2,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,2],[2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],[2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],[2,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,2],[2,0,2,2,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,2],[2,0,2,2,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.grid[14,5]=0
		self.grid[14,22]=0
		#initialize entities
		self.entities = list()
		self.init_entities()
		self.graphics.get_entities(self.entities)
		self.n_games=0
		self.reset()
		
	def reset(self):
		self.number_of_cheeese_eaten=0
		self.frame_iteration = 0
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.grid[14,5]=0
		self.grid[14,22]=0
		self.memory=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],[2,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,2],[2,2,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,2,2],[3,3,3,3,3,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,2,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,2],[2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],[2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],[2,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,2],[2,0,2,2,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,2],[2,0,2,2,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])

		self.score=0
		self.graphics.reset()
		self.graphics.get_grid(self.grid)
		self.debug=True
		self.is_running=True
		self.is_game_over=False
	
	def init_entities(self):
		pacman=Pacman(os.path.join('Assets', 'pac-tmp.png'),name="pacman")
		x,y=self.graphics.grid_to_window(row=23,col=13)
		#x,y=self.graphics.grid_to_window(row=14,col=18)

		rect_dim=16
		offsettino_x=0
		offsettino_y=0
		#offsettino_x=0#7 #29/2
		#offsettino_y=12 #33/2
		pacman.default_x=x#+offsettino_x
		pacman.default_y=y+48#+8
		#offsettino_y+44#36#+48#36
		pacman.set_rect(pacman.default_x,pacman.default_y,rect_dim,rect_dim)
		pacman.set_pos_in_grid()
		self.entities.append(pacman)
		#input()
		#RED
		red=RedGhost(os.path.join('Assets', 'red-tmp.png'),self.grid,name="blinky")
		x,y=self.graphics.grid_to_window(row=11,col=13)
		#offsettino_x=15#//2 #29/2
		#offsettino_y=16#//2 #33/2
		red.default_x=x#+offsettino_x
		red.default_y=y+48#36+offsettino_y
		red.set_rect(red.default_x,red.default_y,rect_dim,rect_dim)
		red.set_pos_in_grid()
		self.entities.append(red)
		#PINK
		pink=PinkGhost(os.path.join('Assets', 'pink-tmp.png'),self.grid,name="pinky")
		x,y=self.graphics.grid_to_window(row=11,col=13)
		pink.default_x=x
		pink.default_y=y+48
		pink.set_rect(pink.default_x,pink.default_y,rect_dim,rect_dim)
		pink.set_pos_in_grid()
		self.entities.append(pink)
	def get_closest_cheese(self):
		#parte da pacman. controlla se a c'è un formaggio su,poi giù, sx e dx. se non c'è parte la ricorsione
		pacman=self.entities[ENTITIES.PACMAN.value]
		y=pacman.pos_in_grid_y
		x=pacman.pos_in_grid_x
		cheese_y=-1
		cheese_x=-1
		cheese_y,cheese_x=self._recursive_cheese(y,x)
		#print("formaggio:"+str(cheese_y)+","+str(cheese_x))
		#input()
		cheese_top=0
		cheese_left=0
		if y<cheese_y:
			cheese_top=1
		if x>cheese_x:
			cheese_left=1		
		return cheese_top,cheese_left
	def _recursive_cheese(self,y,x):
		next_x=x
		next_y=y
		next_y=y-1 #up
		
		found1=self._get_neightbour_cheese(next_y,next_x)
		if found1:
			#print("FOUND")
			result=[next_y,next_x]
			return result[:]
		next_y=y+1 #down
		found2=self._get_neightbour_cheese(next_y,next_x)
		if found2:
			result=[next_y,next_x]
			return result[:]
		next_y=y
		next_x=x-1 #left
		found3=self._get_neightbour_cheese(next_y,next_x)
		if found3:
			result=[next_y,next_x]
			return result[:]
		next_x=x+1 #right
		found4=self._get_neightbour_cheese(next_y,next_x)
		if found4:
			result=[next_y,next_x]
			return result[:]
			
		#print("non ho trovato niente")
		
		if found1 == 0:
			return self._recursive_cheese(y-1,x)
		if found2 == 0:
			return self._recursive_cheese(y+1,x)
		if found3 == 0:
			return self._recursive_cheese(y,x-1)
		if found4 == 0:
			return self._recursive_cheese(y,x+1)
		return [-1,-1] #dovrebbe essere impossibile ma non si sa mai :)
		
	def _get_neightbour_cheese(self,next_y,next_x):
			if next_y<0 or next_y>30 or next_x<0 or next_x>27:
				return -1
			return int(self.grid[next_y][next_x]==1)
		
	def get_neightbours(self,entity):
		y=entity.pos_in_grid_y
		x=entity.pos_in_grid_x
		next_x=x
		next_y=y
		result= []
		#UP
		next_y=y-1
		if next_y<0:
			result.append(0)
		else:
			result.append(self.get_neightbour(next_y,next_x))
		#DOWN
		next_y=y+1
		if next_y>30:
			result.append(0)
		else:
			result.append(self.get_neightbour(next_y,next_x))
		
		next_y=y
		#LEFT
		next_x=x-1
		if next_y==14 and next_x==0: #tp
			result.append(1)
		elif next_x<0:
			result.append(0)
		else:
			result.append(self.get_neightbour(next_y,next_x))
		
		#RIGHT
		next_x=x+1
		if next_y==14 and next_x==27: #tp
			result.append(1)
		elif next_x>27:
			result.append(0)
		else:
			result.append(self.get_neightbour(next_y,next_x))		
		
		return result
	
	def get_neightbour(self,neightbour_y,neightbour_x): #gli ho ordinati così affinché l'ai faccia il ragionamento: grande->meglio
		if self.grid[neightbour_y,neightbour_x]>=2:
			return 0
		if self.grid[neightbour_y,neightbour_x]==0:
			return 1
		if self.grid[neightbour_y,neightbour_x]==1:
			return 2
		
	def check_ghost_is_coming(self,entity): #check if ghost is in line of sight 
		pacman=self.entities[0]
		py=pacman.pos_in_grid_y
		px=pacman.pos_in_grid_x
		ey=entity.pos_in_grid_y
		ex=entity.pos_in_grid_x
		x=0
		y=0
		#check Y danger u
		if px==ex and entity.facing==FACING.SOUTH: 
			dist=py-ey
			if dist>0:
				i=0
				#print("fantasma sopra")
				while i<dist:
					if self.grid[py-i][px]==2:
						y=0
						break
					else:
						y=1
						i+=1
		#check Y danger down
		if px==ex and entity.facing==FACING.NORTH: 
			dist=ey-py
			if dist>0:
				i=0
				#print("fantasma sotto")
				while i<dist:
					if self.grid[py+i][px]==2:
						y=0
						break
					else:
						y=1
						#y=2
						i+=1
		#check X danger left
		if py==ey and entity.facing==FACING.EAST: 
			dist=px-ex
			if dist>0:
				i=0
				#print("fantasma sinistra")
				while i<dist:
					if px==0:
						break
					if	self.grid[py][px-i]==2:
						x=0
						break
					else:
						x=1
						i+=1
		#check x danger right
		if py==ey and entity.facing==FACING.WEST: 
			dist=ex-px
			if dist>0:
				i=0
				#print("fantasma destra")
				while i<dist:
					if px==27:
						break
					if	self.grid[py][px+i]==2:
						x=0
						break
					else:
						#x=2
						x=1
						i+=1
		# height=90
		# width=16
		# entity_long_rect_y= pygame.Rect(entity.rect.x-pacman.rect.height/2,entity.rect.y-height+entity.rect.width/2,width,height*2)
		# pacman_long_rect_y= pygame.Rect(pacman.rect.x-entity.rect.height/2,pacman.rect.y-height+pacman.rect.width/2,width,height*2)
		# entity_long_rect_x= pygame.Rect(entity.rect.x-height+entity.rect.width/2,entity.rect.y-entity.rect.height/2,height*2,width)
		# pacman_long_rect_x= pygame.Rect(pacman.rect.x-height+pacman.rect.width/2,pacman.rect.y-pacman.rect.height/2,height*2,width)
		# y=0
		# x=0
		# if entity_long_rect_y.colliderect(pacman_long_rect_y):
			# pygame.draw.rect(self.graphics.WIN,(200,0,0),entity_long_rect_y)
			# pygame.draw.rect(self.graphics.WIN,(255,0,0),pacman_long_rect_y)
			# pygame.display.update()
			# #if entity.facing==FACING.SOUTH and py > ey:
				# #return True
			# y=1
				# #print("kek s")
			# #if entity.facing==FACING.NORTH and py < ey:
				# #return True
				# #y=1
				# #print("kek n")
		# if entity_long_rect_x.colliderect(pacman_long_rect_x):
			# pygame.draw.rect(self.graphics.WIN,(0, 0, 255),entity_long_rect_x)
			# pygame.draw.rect(self.graphics.WIN,(0,255,0),pacman_long_rect_x)
			# pygame.display.update()
			# #if entity.facing==FACING.WEST and px < ex:
				# #return True
			# x=1
				# #print("kek w")
			# #if entity.facing==FACING.EAST and px > ex:
				# #return True
			# #x=1
				# #print("kek e")
		return y,x, entity.facing
	
	def check_pacman_is_goodboy(self,ghost_facing): #check if pacman is in danger but he is running away
		pf=self.entities[0].facing
		if ghost_facing==FACING.NORTH and pf==FACING.SOUTH:
			return False
		if ghost_facing==FACING.SOUTH and pf==FACING.NORTH:
			return False
		if ghost_facing==FACING.WEST and pf==FACING.EAST:
			return False		
		if ghost_facing==FACING.EAST and pf==FACING.WEST:
			return False
		return True
		
	def check_game_won(self):
		return (1 not in self.grid) # se non c'e' formaggio(1)-> vinto
	def move_entity(self,entity,action):
		rect=entity.rect
		VEL=entity.VEL
		cheese_eaten=False
		ex,ey=entity.window_to_grid()
		ex,ey=self.graphics.grid_to_window(ey,ex)
		#if entity.name=="pacman":
			#print(self.can_move(Actions.LEFT,entity),self.can_move(Actions.RIGHT,entity),self.can_move(Actions.UP,entity),self.can_move(Actions.DOWN,entity))
			#print(rect.x - VEL > 0,rect.x + VEL + rect.width < WIDTH,rect.y - VEL > 0,rect.y + VEL + rect.height < HEIGHT)
			#print( action==Actions.LEFT, action==Actions.RIGHT, action==Actions.UP, action==Actions.UP,action==Actions.UP)
		if action==Actions.LEFT:  # LEFT
		#	if rect.x + rect.width//2 - VEL> 0:
		#		possible_x= entity.rect.x - VEL
		#	else:
		#		possible_x= 0
			if self.can_move(action,entity):
				y=entity.pos_in_grid_y
				x=entity.pos_in_grid_x
				rect.x-=rect.width
				if y==14: 
					if x==0:
						rect.x=WIDTH-rect.width
						
				#entity.rect.x-=VEL
				
				entity.facing= FACING.WEST
		#	else:
				#print("can't move")
				#pass
		elif action==Actions.RIGHT:	# RIGHT
			#if rect.x + rect.width +VEL< WIDTH:
			#	possible_x=entity.rect.x + VEL
			#else:
			#	possible_x = WIDTH-entity.rect.width
			if self.can_move(action,entity):
				y=entity.pos_in_grid_y
				x=entity.pos_in_grid_x
				rect.x+=rect.width
				if y==14: 
					if x==27:
						rect.x=0
			#entity.rect.x+=VEL
				#rect.x+=rect.width
				entity.facing= FACING.EAST
			#else:
				#print("can't move")
				#pass
		elif action==Actions.UP:	# UP
			#if rect.y + rect.height//2 - VEL > 0:
			#	possible_y=entity.rect.y - VEL
			#else:
			#	possible_y = 0 
			if self.can_move(action,entity):
				#entity.rect.y-=VEL
				rect.y-=rect.height
				entity.facing= FACING.NORTH
			#else:
				#print("can't move")
			#	pass
		elif action==Actions.DOWN: # DOWN
			#if rect.y + rect.height + VEL < HEIGHT:
			#if rect.y + rect.height//2 + VEL < HEIGHT:
			#	possible_y=entity.rect.y + VEL #rect.height//2 + VEL
			#else:
			#	possible_y=HEIGHT-rect.height//2
			if self.can_move(action,entity):
				#entity.rect.y+=VEL
				rect.y+=rect.height
				#entity.rect.y=possible_y
				entity.facing= FACING.SOUTH
			#else:
				#print("can't move")
			#	pass
		
		entity.pos_in_grid_x,entity.pos_in_grid_y=entity.window_to_grid()
		if entity.name=="pacman": #eat cheese
			#print(self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x])
			if self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x]==1:
				cheese_eaten=True
				self.number_of_cheeese_eaten+=1
			self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x]=0
			self.memory[entity.pos_in_grid_y][entity.pos_in_grid_x]=1
			
		
		return cheese_eaten
	#DIPENDENZA CLASSE GRAPHICS ROTTA
	def can_move(self,action,entity):
		#print(self.graphics.window_to_grid(entity.rect.x,entity.rect.y))
		#return True #TODO
		#print(action,entity)
		#x=(possible_x+30//2)//16
		#y=(possible_y+30//2)//16
		#print(y,x)
		x,y=entity.window_to_grid()
		next_y=y
		next_x=x
		#VEL=entity.VEL
		#rect=entity.rect
		#print(rect.bottom)
		#pixel_x,pixel_y=self.graphics.grid_to_window(y,x)
		
		#pixelx=0
		#pixel_y=0
		#signoreIddioy=6
		#signoreIddiox=4
		#pixel_y+=6#offsettino_y//2
		#pixel_x+=4#offsettino_x//2
		if action == Actions.UP: #and y<0:
			next_y=y-1
			#pixel_y=rect.x#-entity.rect.height//2
			#pixel_next_y=pixel_y-VEL#-signoreIddioy
			#pixel_next_x=rect.x
			# return False
		if action == Actions.DOWN: #and y>29:
			next_y=y+1
			#pixel_y=rect.y-rect.height#rect.bottom
			#pixel_next_y=pixel_y+VEL
			#pixel_next_x=pixel_x
			# return False
		if action == Actions.LEFT: #and y<0:
			next_x=x-1
			#pixel_x=rect.x#-entity.rect.width//2
			#pixel_next_x=pixel_x-VEL
			#pixel_next_y=pixel_y
			#pixel_next_x=pixel_x
			# return False
		if action == Actions.RIGHT: #and y>26:
			next_x=x+1
			#print(rect.right)
			#print(rect.x,rect.right,rect.width)
			#pixel_x=rect.x+entity.rect.width#//2
			#pixel_next_x=pixel_x+VEL
			#pixel_next_y=pixel_y
		
		if action == Actions.HALT:
			return False
			# return False
		
		#print(pixel_next_y,pixel_next_x)
		#wx,wy=self.graphics.window_to_grid(pixel_next_x,pixel_next_y)
		#print(self.graphics.grid_to_window(y,x),pixel_x,pixel_next_y)
		# if action == Actions.UP and self.grid[y-1,x]==2:
			# #wx,wy=self.graphics.grid_to_window(y+1,x)
			# #y=entity.rect.y-entity.rect.height//2
			# #rimettere
			# if pixe
			#if y > wy :
				# return True
			# return False
		# if action == Actions.DOWN and self.grid[y+1,x]==2:
			# #wx,wy=self.graphics.grid_to_window(y+1,x)
			# #y=entity.rect.y#+entity.rect.height
			# #print(y,wy)
			# if pixel_y < wy :
				# return True
			# return False
		# if action == Actions.LEFT and self.grid[y,x-1]==2:
			# #wx,wy=self.graphics.grid_to_window(y,x-1)
			# x=entity.rect.x-entity.rect.width//2
			# #rimettere
			# #	return True
			# if pixel_x > wx :
				# return True
			# return False
		# if action == Actions.RIGHT and self.grid[y,x+1]==2:
			# #wx,wy=self.graphics.grid_to_window(y,x+1)
			# #x=entity.rect.x#+entity.rect.width
			# if pixel_x < wx :
				# return True
			# return False
		
		# return True
		#wx,wy=self.graphics.window_to_grid(nex,pixel_next_y)
		#print(wy,wx,self.grid[wy,wx])
		#print(y,x,next_y,next_x)
		#entity takes the tunnel
		if next_y==14: 
			if next_x==-1:
				return True
				#next_x=9
				#print("tippo")
			if next_x==28:
				return True
				#print("tippo")
			
		if next_y<0 or next_y>30 or next_x<0 or next_x>27:
			return False
		if self.grid[next_y,next_x]==2:
			#print("can't move: "+ Actions(action).name)
			#print("muro")
			#print(y,x,wy,wx)
			#print(self.graphics.grid_to_window(y,x),pixel_x,pixel_next_y)
			return False
		return True
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

	def play_step(self,action):
		self.graphics.frame_iteration+=1
		#print(self.graphics.frame_iteration,self.graphics.old_iter)
		#sicurezza= distanza fantasma-pacman? e punisco quando la sicurezza diminuisce 
		#print(action)
		pacman=self.entities[ENTITIES.PACMAN.value]
		if self.graphics.timer <2.5:
			#return #il timer lo abilito nella release, mentre sviluppo e' una perdita di tempo
			pass 
		
		if self.graphics.frame_iteration>self.graphics.old_iter+6:
			self.graphics.old_iter=self.graphics.frame_iteration
			#print("muovo")
			for entity in self.entities: #for each ghost
				if entity.name == "pacman":
					continue	
				dy,dx=entity.get_new_path(self.entities[ENTITIES.PACMAN.value])
				#LEGENDA: px=pacman_x,dx=destion_x (next step in path),ex=entity_x (ghost)
				#dy,dx=entity.get_new_path(px,py) #where am i going to move
				ex=entity.pos_in_grid_x
				ey=entity.pos_in_grid_y
				#print("sono a: "+str(ey)+","+str(ex)+" e voglio andare a: "+str(dy)+","+str(dx))
				#print(dx)
				if dx==-2: #dovrebbe sempre trovare il path, questo if e' in caso l'universo si distrugga
					print("error")
					continue
				if dx==-1:
					dx=pacman.pos_in_grid_x
					dy=pacman.pos_in_grid_y
					#print("error")
					#continue
				ghost_action=self.coords_to_direction(ex,ey,dx,dy)
				self.move_entity(entity,ghost_action)

		reward=0
		game_over=0
		#print("sono a: "+str(pacman.pos_in_grid_y)+","+str(pacman.pos_in_grid_x)+" e voglio andare " + str(action))
		#print("game: "+str(action))
		if self.have_i_been_here_before(action,self.entities[ENTITIES.PACMAN.value]):
				reward-=10 #+pow(1.01,self.number_of_cheeese_eaten)
		cheese_eaten= self.move_entity(pacman,action)
		if cheese_eaten:
			self.score+=10
			reward=30 + pow(1.03,self.number_of_cheeese_eaten)
		if self.check_game_won():
			self.score+=1000
			game_over=1
		#if not self.can_move(action,entity) and action!= Actions.HALT:
		#	reward+=-3
		#	print("can't move: "+ Actions(action).name)
		#else:
		#	reward=-5
		#se sono in pericolo (non è preciso perché ignora i muri) allora non ti premio
		#red=self.entities[ENTITIES.RED.value]
		for entity in self.entities:
			if entity.name=="pacman":
				continue
			danger_y,danger_x,ghost_facing=self.check_ghost_is_coming(entity)
			#is_goodboy=self.check_pacman_is_goodboy(ghost_facing)
			if danger_y: #and not is_goodboy:
				reward+=-40
			if danger_x:# and not is_goodboy:
				reward+=-40
			#if is_goodboy:
			#	reward+=10s
		if self.check_game_over():
			reward=-500
			game_over=1
			self.n_games+=1
		self.graphics.draw_window(self.debug)
		#print(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
		#print(reward)
		return reward, game_over, self.score	
	def check_game_over(self):
		pacman=self.entities[ENTITIES.PACMAN.value]
		for entity in self.entities:
			#print(entity.name+": "+str(entity.pos_in_grid_y)+","+str(entity.pos_in_grid_x)+"\t pacman: "+str(pacman.pos_in_grid_y)+","+str(pacman.pos_in_grid_x))
			if entity.name !="pacman":
				if entity.pos_in_grid_x== pacman.pos_in_grid_x and entity.pos_in_grid_y == pacman.pos_in_grid_y:
				#e_rect=pygame.Rect(entity.rect.x,entity.rect.y,*entity.IMAGE.get_size())
				#p_rect=pygame.Rect(pacman.rect.x,pacman.rect.y,*pacman.IMAGE.get_size())
				#if p_rect.colliderect(e_rect):
				#	self.game_over=True
					return True
			
		return False
			#if entity.pos_in_grid_y== pacman.pos_in_grid_y and entity.pos_in_grid_x==pacman.pos_in_grid_x:
			#		return True
		#return False
				#if pacman.rect.colliderect(entity.rect):
					#self.game_over=True
				#	return True
		if self.grid[pacman.pos_in_grid_y][pacman.pos_in_grid_x]>1:
			print("WTF")
			return True
		#self.game_over=False
		return False
	#def can_move_neighbours_cells(self,entity):
	#	 return self.can_move(Actions.LEFT,entity),self.can_move(Actions.RIGHT,entity),self.can_move(Actions.UP,entity),self.can_move(Actions.DOWN,entity)
	
	def cheese_per_action(self,action,entity):
		x=entity.pos_in_grid_x
		y=entity.pos_in_grid_y
		n=0
		for k in range(1):
			y=y+k
			if y>30:
				y=30
			#print(y)
			cell=self.grid[y][x]
			#print(y,cell)
			#print(cell)
			if action==Actions.LEFT:
				while x>-1 and cell!=2:
					x-=1
					cell=self.grid[y][x]
					if cell == 1:
						n=n+1
			if action==Actions.RIGHT:
				while x<27 and cell!=2:
					x+=1
					cell=self.grid[y][x]
					if cell == 1:
						n=n+1
			if action==Actions.UP:
				while y>-1 and cell!=2:
					y-=1
					cell=self.grid[y][x]
					if cell == 1:
						n=n+1
			if action==Actions.DOWN:
				while y<30 and cell!=2:
					y+=1
					cell=self.grid[y][x]
					if cell == 1:
						n=n+1
		return n
	
	def have_i_been_here_before(self,action,entity):
		y=entity.pos_in_grid_y
		x=entity.pos_in_grid_x
		next_y=y
		next_x=x

		if action == Actions.UP: #and y<0:
			next_y=y-1

		if action == Actions.DOWN: #and y>29:
			next_y=y+1

		if action == Actions.LEFT: #and y<0:
			next_x=x-1
		if action == Actions.RIGHT: #and y>26:
			next_x=x+1
		
		if action == Actions.HALT:
			return 1
		
		if next_y<0 or next_y>30 or next_x<0 or next_x>27:
			return 0
		if self.memory[next_y,next_x]==0:
			return 0
		return 1
def main():

	game= Game()
	while True:
		check_for_events(game)
		if not game.is_running:
			continue
		keys_pressed = pygame.key.get_pressed()
		#game.clock.tick(FPS)
		#game.frame_iteration+=1
		game.graphics.update_time(game.frame_iteration/60)
		game.graphics.draw_window(game.debug)
		action=check_keyboard() #questo ora e manuale, poi ci pensera' l'agents
		game.play_step(action) #ignorare il parametro per ora
		#print(game.score)
		if game.check_game_over():
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
					game.n_games+=1
					
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
