from cmath import sqrt
from difflib import restore
from html import entities
import time
from tkinter import RIGHT
import pygame
import os
import sys
from enum import Enum
import numpy as np
from entities import Entity, Pacman, RedGhost, PinkGhost, FACING
import graphics as gp
import heapq
from pathfinding import solver
from math import sqrt as float_sqrt
from pygame import mixer

GHOST_SPEED=6

class FACING(Enum):
	NORTH = 0
	SOUTH= 1
	WEST = 2
	EAST= 3


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
def compare_int(a,b):
	if a>b: 
		return 1
	if a==b:
		return 0
	return -1
def do_i_have_a_third_exit(entity,next_action):
	y_mod= -1 if next_action== Actions.UP else +1 if next_action== Actions.UP else 0
	x_mod= -1 if next_action== Actions.LEFT else +1 if next_action== Actions.RIGHT else 0
	y=entity.pos_in_grid_y+y_mod
	x=entity.pos_in_grid_x+x_mod
	y=entity.pos_in_grid_y
	x=entity.pos_in_grid_x
	safe_points=np.array([[1,6],[1,21],[5,1],[5,6],[5,9],[5,12],[5,15],[5,18],[5,21],[8,6],[8,21],[11,12],[11,15],[14,6],[14,9],[14,18],[14,21],[17,9],[17,18],[20,6],[20,9],[20,18],[20,21],[23,6],[23,9],[23,12],[23,15],[23,18],[23,21],[26,3],[26,24],[29,12],[29,15]])
	return ([y, x] == safe_points).all(1).any()
def is_in_turning_point(entity):
		y=entity.pos_in_grid_y
		x=entity.pos_in_grid_x
		turning_points=np.array([[1,1],[1,6],[1,12],[1,15],[1,21],[1,26],[5,1],[5,6],[5,9],[5,12],[5,15],[5,18],[5,21],[5,26],[8,1],[8,6],[8,9],[8,12],[8,15],[8,18],[8,21],[8,26],[11,9],[11,12],[11,15],[11,18],[14,6],[14,9],[14,18],[14,21],[17,9],[17,18],[20,1],[20,6],[20,9],[20,12],[20,15],[20,18],[20,21],[20,26],[23,1],[23,3],[23,6],[23,9],[23,12],[23,15],[23,18],[23,21],[23,24],[23,26],[26,1],[26,3],[26,6],[26,9],[26,12],[26,15],[26,18],[26,21],[26,24],[26,26],[29,1],[29,12],[29,15],[29,26]])
		return ([y, x] == turning_points).all(1).any() 

class Game():
	def __init__(self, w=WIDTH, h=HEIGHT):
		self.w=w
		self.h=h
		self.frame_iteration = 0
		self.game_started= False
		self.graphics = gp.PacGraphic(w,h)
		self.graphics.FPS=60 #MAX FPS
		#0=clear_path,2=wall,1=coin,3=invalid
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.grid[14,5]=0
		self.grid[14,22]=0
		self.entities = []
		self.init_entities()
		self.graphics.get_entities(self.entities)
		self.n_games=0
		self.s= solver(self.grid)
		pygame.mixer.music.load(os.path.join('Assets', 'Sfx', 'game_start.wav'))
		pygame.mixer.music.set_volume(0.05)
		self.played_start = False
		self.ready_image = pygame.image.load(os.path.join('Assets', 'ready.png'))
		self.quit = False
		self.reset()
		
	def reset(self):
		self.red_distance_lvl=4
		self.pink_distance_lvl=4
		self.sandwitch=1
		self.cheese_zone_y=1
		self.cheese_zone_x=0
		self.pacman_zone_y=1
		self.pacman_zone_x=0
		self.last_meaninful_action=-1 #halt
		self.exit_top=0
		self.exit_left=0
		self.cheese_left=1
		self.cheese_top=1
		self.stuck=0
		self.red_getting_closer=0
		self.pink_getting_closer=0
		self.number_of_cheeese_eaten=0
		self.frame_iteration = 0
		#self.unsure=0
		self.safe_exit=1
		self.cheese_dist=0
		self.is_game_over=0
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.grid[14,5]=2
		self.grid[14,22]=2

		self.score=0
		self.graphics.reset()
		self.graphics.get_grid(self.grid)
		self.debug=False
		self.is_running=True
		self.is_game_over=False
		#self.possibilities=[1,1,1,1]
		self.possibilities=[-1,-1,-1,-1]
		#self.in_corner=[0,0,0,0]
		self.red_in_corner=[0,0,0,0]
		self.pink_in_corner=[0,0,0,0]
		self.can_go_in_there_before_ghost_new()
	def set_powerups(self):
			self.grid[3,1]=-1
			self.grid[3,26]=-1
			self.grid[23,1]=-1
			self.grid[23,26]=-1


	def init_entities(self):
		#PAC
		pacman=Pacman(os.path.join('Assets', 'Pac_Sprites.png'),name="pacman")
		x,y=self.graphics.grid_to_window(row=23,col=13)
		rect_dim=16
		pacman.default_x=x
		pacman.default_y=y+48
		pacman.set_rect(pacman.default_x,pacman.default_y,rect_dim,rect_dim)
		pacman.set_pos_in_grid()
		self.entities.append(pacman)
		#RED
		red=RedGhost(os.path.join('Assets', 'Red_Sprites.png'),self.grid,name="blinky")
		x,y=self.graphics.grid_to_window(row=11,col=12)
		red.default_x=x
		red.default_y=y+48
		red.set_rect(red.default_x,red.default_y,rect_dim,rect_dim)
		red.set_pos_in_grid()
		self.entities.append(red)
		#PINK
		pink=PinkGhost(os.path.join('Assets', 'Pink_Sprites.png'),self.grid,name="pinky")
		x,y=self.graphics.grid_to_window(row=11,col=15)
		pink.default_x=x
		pink.default_y=y+48
		pink.set_rect(pink.default_x,pink.default_y,rect_dim,rect_dim)
		pink.set_pos_in_grid()
		self.entities.append(pink)

	def am_i_regretting(self,pacman,next_action):
		mistake_before=0
		if self.last_meaninful_action != Actions.HALT:
			mistake_before=not self.can_move(self.last_meaninful_action,pacman)
		if mistake_before:
			return 0
		if (self.last_meaninful_action==2 and next_action==Actions.RIGHT) or (self.last_meaninful_action==3 and next_action==Actions.LEFT):
			return 1
		if (self.last_meaninful_action==0 and next_action==Actions.DOWN) or (self.last_meaninful_action==1 and next_action==Actions.UP):
			return 1
		return 0

	def can_go_in_there_before_ghost_new(self):
		py=self.entities[0].pos_in_grid_y
		px=self.entities[0].pos_in_grid_x
		red=self.entities[1]
		pink=self.entities[2]
		self.possibilities=[99,99,99,99]
		#calculate delta_pacman_tile
		delta_pacman_tile=[0,0,0,0]
		four_direction=self.where_entity_is_looking(py,px)
		for i,coords in enumerate(four_direction):
			dist=float_sqrt(pow(abs(py-coords[0]),2)+pow(abs(px-coords[1]),2))
			delta_pacman_tile[i]=dist
		
		#calculate delta_ghost_tile, the smallest dist will be put in self.possibilities
		for ghost in [red,pink]:
			ghost_looking_at=self.where_entity_is_looking(ghost.pos_in_grid_y,ghost.pos_in_grid_x)
			for i in range(4):
				if (four_direction[i][0],four_direction[i][1]) in ghost.path or (four_direction[i][0],four_direction[i][1])==(py,px): 
					delta_ghost_tile=ghost.distance_from_pacman-delta_pacman_tile[i]-1
				else:
					delta_ghost_tile=ghost.distance_from_pacman+delta_pacman_tile[i]-1
					if (self.ghost_between_tile_pacman(ghost,four_direction[i][0],four_direction[i][1],i)):
						delta_ghost_tile=ghost.distance_from_pacman-delta_pacman_tile[i]-1

				diff=abs(delta_ghost_tile-delta_pacman_tile[i])
				if (four_direction[i][0],four_direction[i][1])==(py,px): #if pacman looking at its current pos
					diff=0 #just to impact the reward
				pos=delta_ghost_tile-delta_pacman_tile[i]>=0
				if (self.possibilities[i]>diff and pos) or (self.possibilities[i]>0 and not pos) or (self.possibilities[i]<0 and abs(self.possibilities[i])<diff):
					if not pos:
						diff=-diff
					self.possibilities[i]= int(diff)
		


	def can_go_in_there_before_ghost(self):
		pacman=self.entities[0]
		red=self.entities[1]
		pink=self.entities[2]
		py=pacman.pos_in_grid_y
		px=pacman.pos_in_grid_x

		self.possibilities=[1,1,1,1]
	
		self.red_in_corner=[0,0,0,0]
		self.pink_in_corner=[0,0,0,0]
		four_direction=self.where_entity_is_looking(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
		for ghost_index,ghost in enumerate([red,pink]):
			gy=ghost.pos_in_grid_y
			gx=ghost.pos_in_grid_x
			tmp=self.is_ghost_in_the_corner(ghost,pacman)
			g_dist=ghost.distance_from_pacman
			danger_y,danger_x,facing=self.check_ghost_is_coming(ghost)
			for index in range(4): 
				if tmp[index]: #prevent second ghost ovveride  
					if ghost_index==0:
						self.red_in_corner[index]=1
					else:
						self.pink_in_corner[index]=1
				if ((four_direction[index][0],four_direction[index][1])==(pacman.pos_in_grid_y,pacman.pos_in_grid_x)):
						self.possibilities[index]=0
						continue
				if not danger_x and not danger_y:
					continue
				if 	(index<2 and danger_y):
						p_dist=abs(py-four_direction[index][0])+2
						g_dist=abs(gy-four_direction[index][0])
						if g_dist<=p_dist:
							self.possibilities[index]=0
							continue
				if 	(index>=2 and danger_x):
					p_dist=abs(px-four_direction[index][1])+2
					g_dist=abs(gx-four_direction[index][1])
					if g_dist<=p_dist:
						self.possibilities[index]=0
						continue
			

		for i in range(4):
			self.possibilities[i]=int(self.possibilities[i] and not (self.red_in_corner[i] or  self.pink_in_corner[i]))
	
	def is_ghost_in_the_corner(self,ghost,pacman):
		"""restituisce 1 array boolean [N,S,W,O] se 0=puoi andare lì senza che ghost sia in agguato"""
		pacman_looking_at= self.where_entity_is_looking(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
		ghost_looking_at= self.where_entity_is_looking(ghost.pos_in_grid_y,ghost.pos_in_grid_x)
		index=0
		if ghost.facing==FACING.NORTH:
			index=0
		if ghost.facing==FACING.SOUTH:
			index=1
		if ghost.facing==FACING.WEST:
			index=2
		if ghost.facing==FACING.EAST:
			index=3
		
		tuple_of_array = np.where((pacman_looking_at == ghost_looking_at[index]).all(axis=1))
		result= [0,0,0,0]
		for array in tuple_of_array:
			if index<2 and ghost.pos_in_grid_x==pacman.pos_in_grid_x:
				continue
			if index>=2 and ghost.pos_in_grid_y==pacman.pos_in_grid_y:
				continue
			for index in array:
				if not (pacman_looking_at[index][0]==pacman.pos_in_grid_y and pacman_looking_at[index][1]==pacman.pos_in_grid_x):
					result[index]=1
		return result
			
			
	def is_in_turning_point(self,y,x):
		turning_points=np.array([[1,1],[1,6],[1,12],[1,15],[1,21],[1,26],[5,1],[5,6],[5,9],[5,12],[5,15],[5,18],[5,21],[5,26],[8,1],[8,6],[8,9],[8,12],[8,15],[8,18],[8,21],[8,26],[11,9],[11,12],[11,15],[11,18],[14,6],[14,9],[14,18],[14,21],[17,9],[17,18],[20,1],[20,6],[20,9],[20,12],[20,15],[20,18],[20,21],[20,26],[23,1],[23,3],[23,6],[23,9],[23,12],[23,15],[23,18],[23,21],[23,24],[23,26],[26,1],[26,3],[26,6],[26,9],[26,12],[26,15],[26,18],[26,21],[26,24],[26,26],[29,1],[29,12],[29,15],[29,26]])
		return ([y, x] == turning_points).all(1).any()		


	def where_entity_is_looking(self,y,x):
		result = []
		ey=y
		ex=x

		i=1
		#NORTH
		while self.grid[ey-i,ex]!=2:
			if self.is_in_turning_point(ey-i,ex):
				i+=1
				break
			i+=1
		result.append([ey-i+1,ex])
		i=1
		#SOUTH
		while self.grid[ey+i,ex]!=2:
			if self.is_in_turning_point(ey+i,ex):
				i+=1
				break
			i+=1
		result.append([ey+i-1,ex])
		#WEST
		i=1
		while self.grid[ey,ex-i]!=2:
			if ex-i==0:
				ex=20
				i=0
				break	
			if self.is_in_turning_point(ey,ex-i):
				i+=1
				break
			i+=1
		result.append([ey,ex-i+1])
		i=1
		ex=x
		if ex==27:
			ex=0
		#EAST
		while self.grid[ey,ex+i]!=2:
			if ex+i==27:
				ex=7
				i=0
				break
			if self.is_in_turning_point(ey,ex+i):
				i+=1
				break
			i+=1
		result.append([ey,ex+i-1])

		return np.array(result)

	def get_closest_safe_exit(self):
		py=self.entities[0].pos_in_grid_y
		px=self.entities[0].pos_in_grid_x
		safe_points=np.array([[1,6],[1,21],[5,1],[5,6],[5,9],[5,12],[5,15],[5,18],[5,21],[8,6],[8,21],[11,12],[11,15],[14,6],[14,9],[14,18],[14,21],[17,9],[17,18],[20,6],[20,9],[20,18],[20,21],[23,6],[23,9],[23,12],[23,15],[23,18],[23,21],[26,3],[26,24],[29,12],[29,15]])
		exits = np.array([])
		for coords in safe_points:
			dist=float_sqrt(pow(abs(py-coords[0]),2)+pow(abs(px-coords[1]),2))
			exits=np.append(exits, np.array([[coords[0],coords[1],dist]]))
		
		exits=exits.reshape(33,3)
		exits=exits[exits[:, 2].argsort()]
		dghost=[self.entities[1].distance_from_pacman,self.entities[2].distance_from_pacman]
		for i in range(8):
			next_tile_to_get_there,exits[i][2]=self.s.get_path(py,px,int(exits[i][0]),int(exits[i][1]))
			if next_tile_to_get_there==(-1,-1): #safe exit == pacman pos
				self.exit_top=0
				self.exit_left=0
				return
			index_of_possibilities=-1 #up,down,left,right
			for index,mod in enumerate([[-1,0],[+1,0],[0,-1],[0,+1]]):
				if ((py+mod[0]),(px+mod[1]))==next_tile_to_get_there:
					index_of_possibilities=index
					break			
			if  dghost[0]-exits[i][2]>0 and dghost[0]-exits[i][2]>0:
				if self.possibilities[index_of_possibilities] :
					self.exit_top=compare_int(py,exits[i][0])
					self.exit_left=compare_int(px,exits[i][1])
				return		
		#there is no safe exit that can be reach without dying
		self.exit_top=-2
		self.exit_left=-2

	def get_closest_cheese(self):
		if self.check_game_won():
			return 0,0,0
		pacman=self.entities[ENTITIES.PACMAN.value]
		y=pacman.pos_in_grid_y
		x=pacman.pos_in_grid_x
		self.BEST=[-1,-1,999]
		self._recursive_cheese(y,x,0,(pacman.facing.value)+1)
 
		cheese_y=self.BEST[0]
		cheese_x=self.BEST[1]
		cheese_dist=self.BEST[2]
		cheese_top=compare_int(y,cheese_y)
		cheese_left=compare_int(x,cheese_x)
		return cheese_top,cheese_left,cheese_dist

	def compare_distance_of_all_cheese(self):
		py=self.entities[0].pos_in_grid_y
		px=self.entities[0].pos_in_grid_x
		cheese_coords=np.array(np.where(self.grid==1)).T #get all coords where there is cheese
		self.BEST=[0,0,999]
		for coords in cheese_coords:
			dist=float_sqrt(pow(abs(py-coords[1]),2)+pow(abs(px-coords[0]),2))
			if dist < self.BEST[2]:
				self.BEST=[coords[1],coords[0],dist]

	def _recursive_cheese(self,y,x,dist,prev_direction):

		if dist>35: #if cheese is too far, switch to fastest (and worse) algorithm
			return self.compare_distance_of_all_cheese()

		found1=-1
		found2=-1
		found3=-1
		found4=-1
		next_x=x
		next_y=y
		next_y=y-1 #up
		if prev_direction!= 2:
			found1=self._get_neightbour_cheese(next_y,next_x)
		if found1==1:
			if dist+1<self.BEST[2]:
				self.BEST=[next_y,next_x,dist+1]
			return
		next_y=y+1 #down
		if prev_direction!= 1:
			found2=self._get_neightbour_cheese(next_y,next_x)
		if found2==1:
			if dist+1<self.BEST[2]:
				self.BEST=[next_y,next_x,dist+1]
			return
		next_y=y
		next_x=x-1 #left
		if prev_direction !=4:
			found3=self._get_neightbour_cheese(next_y,next_x)
		if found3==1:
			if dist+1<self.BEST[2]:
				self.BEST=[next_y,next_x,dist+1]
			return
		next_x=x+1 #right
		if prev_direction !=3:
			found4=self._get_neightbour_cheese(next_y,next_x)
		if found4==1:
			if dist+1<self.BEST[2]:
				self.BEST=[next_y,next_x,dist+1]
			return
		if found1 == 0:
			if dist+1<self.BEST[2]:
				self._recursive_cheese(y-1,x,dist+1,1)
			
		if found2 == 0:
			if dist+1<self.BEST[2]:
				self._recursive_cheese(y+1,x,dist+1,2)
		if found3 == 0:
			if dist+1<self.BEST[2]:
				self._recursive_cheese(y,x-1,dist+1,3)

		if found4 == 0:
			if dist+1<self.BEST[2]:
				self._recursive_cheese(y,x+1,dist+1,4)
		
	def _get_neightbour_cheese(self,next_y,next_x):
			if next_y<0 or next_y>30 or next_x<0 or next_x>27:
				return -1
			if self.grid[next_y][next_x] in [-1,1]:
				return 1
			if self.grid[next_y][next_x]==0:
				return 0
			if self.grid[next_y][next_x]==2:
				return -1


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
	
	def get_neightbour(self,neightbour_y,neightbour_x):
		"""returns the array of neightbour cells. the bigger the value the more precious the cell"""
		if self.grid[neightbour_y,neightbour_x]>=2:
			return 0
		if self.grid[neightbour_y,neightbour_x]==0:
			return 1
		if self.grid[neightbour_y,neightbour_x]==1:
			return 2
	
	def check_ghost_is_coming(self,entity):
		"""check if ghost is in line of sight """
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
				while i<dist:
					if self.grid[py+i][px]==2:
						y=0
						break
					else:
						y=1
						i+=1
		#check X danger left
		if py==ey and entity.facing==FACING.EAST: 
			dist=px-ex
			if dist>0:
				i=0
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
				while i<dist:
					if px==27:
						break
					if	self.grid[py][px+i]==2:
						x=0
						break
					else:
						x=1
						i+=1
		return y,x, entity.facing
		
	def check_game_won(self):
		"""if no cheese tiles -> game is won"""
		return (1 not in self.grid)

	def move_entity(self,entity,action):
		rect=entity.rect
		cheese_eaten=False
		ex,ey=entity.window_to_grid()
		ex,ey=self.graphics.grid_to_window(ey,ex)
		entity.old_action=action
		if action==Actions.LEFT:  # LEFT
			if self.can_move(action,entity):
				y=entity.pos_in_grid_y
				x=entity.pos_in_grid_x
				rect.x-=rect.width
				if y==14: 
					if x==0:
						rect.x=WIDTH-rect.width
				entity.facing= FACING.WEST

		elif action==Actions.RIGHT:	# RIGHT
			if self.can_move(action,entity):
				y=entity.pos_in_grid_y
				x=entity.pos_in_grid_x
				rect.x+=rect.width
				if y==14: 
					if x==27:
						rect.x=0
				entity.facing= FACING.EAST

		elif action==Actions.UP:	# UP

			if self.can_move(action,entity):
				rect.y-=rect.height
				entity.facing= FACING.NORTH
		elif action==Actions.DOWN: # DOWN

			if self.can_move(action,entity):
				rect.y+=rect.height
				entity.facing= FACING.SOUTH
		
		entity.pos_in_grid_x,entity.pos_in_grid_y=entity.window_to_grid()
		if entity.name=="pacman": #eat cheese
			if action!=Actions.HALT:
				self.last_meaninful_action=0 if action==Actions.UP else 1 if action==Actions.DOWN else 2 if action==Actions.LEFT else 3 if action==Actions.RIGHT else -1 
			if self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x]==1:
				cheese_eaten=True
				self.number_of_cheeese_eaten+=1
				if pygame.mixer.music.get_busy():
					pygame.mixer.music.queue(os.path.join('Assets', 'Sfx', 'munch_lungo.wav'))
				else:
					pygame.mixer.music.play()
			self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x]=0
			
		
		return cheese_eaten

	def can_move(self,action,entity):

		x,y=entity.window_to_grid()
		next_y=y
		next_x=x
		if action == Actions.UP:
			next_y=y-1

		if action == Actions.DOWN:
			next_y=y+1
		if action == Actions.LEFT: #and y<0:
			next_x=x-1
		if action == Actions.RIGHT:
			next_x=x+1

		
		if action == Actions.HALT:
			return True
			
		if next_y<0 or next_y>30 or next_x<0 or next_x>27:
			return False
		if self.grid[next_y,next_x]==2:
			return False
		return True

	def coords_to_direction(self,x,y,dx,dy):
		if x>dx:
			return Actions.LEFT
		if x<dx:
			return Actions.RIGHT
		if y<dy:
			return Actions.DOWN
		if y>dy:
			return Actions.UP
		
	def play_ghost(self):

		self.graphics.frame_iteration+=1

		pacman=self.entities[ENTITIES.PACMAN.value]
		if self.graphics.frame_iteration>self.graphics.old_iter+GHOST_SPEED:
			self.graphics.old_iter=self.graphics.frame_iteration
			for entity in self.entities[1:]: #for each ghost
				dy,dx=entity.get_new_path(pacman)
				ex=entity.pos_in_grid_x
				ey=entity.pos_in_grid_y
				if dx==-1:
					dx=pacman.pos_in_grid_x
					dy=pacman.pos_in_grid_y
				ghost_action=self.coords_to_direction(ex,ey,dx,dy)
				self.move_entity(entity,ghost_action)
		self.check_game_over()

	def play_step(self,action):
		reward=0
		self.check_game_over()
		pacman=self.entities[ENTITIES.PACMAN.value]
		red=self.entities[1]
		pink=self.entities[2]
		if self.is_game_over:
				reward=-10000
				self.n_games+=1
				return reward, self.is_game_over, self.score

		self.get_closest_safe_exit()
		self.stuck=int(self.am_i_regretting(pacman,action))
		toppest_ghost_y=min(red.pos_in_grid_y,pink.pos_in_grid_y)
		leftest_ghost_x=min(red.pos_in_grid_x,pink.pos_in_grid_x)

		if action==Actions.UP:
			if toppest_ghost_y<pacman.pos_in_grid_y:
				reward+=-10
			if toppest_ghost_y>pacman.pos_in_grid_y:
				reward+=+10
		if action==Actions.DOWN:
			if toppest_ghost_y>pacman.pos_in_grid_y:
				reward+=-10
			if toppest_ghost_y<pacman.pos_in_grid_y:
				reward+=+10
		if action==Actions.LEFT:
			if leftest_ghost_x<pacman.pos_in_grid_x:
				reward+=-10
			if leftest_ghost_x>pacman.pos_in_grid_x:
				reward+=+10
		if action==Actions.RIGHT:
			if leftest_ghost_x>pacman.pos_in_grid_x:
				reward+=-10
			if leftest_ghost_x<pacman.pos_in_grid_x:
				reward+=+10
		self.can_go_in_there_before_ghost_new()
		self.safe_exit=do_i_have_a_third_exit(pacman,action)
		
		self.sandwitch=self.am_i_in_sandwitch()	
		if not self.can_move(action,pacman):
			reward+=-2000
		if self.stuck:
			reward+=-700
		inting_lists=[ [Actions.UP,Actions.HALT], [Actions.DOWN,Actions.HALT], [Actions.LEFT,Actions.HALT],[Actions.RIGHT,Actions.HALT]]
		for i in range(4):
			if action in inting_lists[i]:
				if action==Actions.HALT and self.safe_exit:
					break
				if self.possibilities[i]<0 and pacman.facing.value == i:  #if inting
	
					reward+=-1000
		
		if min(red.distance_from_pacman,pink.distance_from_pacman)<3: #ghost is really close to me	
			reward+=-1000
		if min(red.distance_from_pacman,pink.distance_from_pacman)<7: #ghost is kinda close to me
			reward+=-1000

		if not self.safe_exit:
			if self.exit_top==1 and action in [Actions.UP]:
				reward+=20
			elif self.exit_top==-1 and action in [Actions.DOWN]:
				reward+=20
			elif self.exit_left==1 and action in [Actions.LEFT]:
				reward+=20
			elif self.exit_left==-1 and action in [Actions.RIGHT]:
				reward+=20
		cheese_eaten= self.move_entity(pacman,action)
		
		self.cheese_top,self.cheese_left,dist=self.get_closest_cheese()

		if cheese_eaten:
			self.score+=10
			reward+=1800			

		self.check_game_over()
		if self.is_game_over:
				reward=-10000
				self.n_games+=1

		if self.check_game_won():
		
			self.n_games+=1
			self.is_game_over=1

		self.graphics.draw_window(self.debug,self.score)

		if self.played_start == False:
			self.played_start = True
			rect = self.ready_image.get_rect()
			rect.center = (225,330)
			self.graphics.WIN.blit(self.ready_image,rect)
			pygame.display.update()
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy():
				continue
			pygame.mixer.music.load(os.path.join('Assets', 'Sfx', 'munch_lungo.wav'))

		return reward, self.is_game_over, self.score	
	
	def ghost_between_tile_pacman(self,ghost,tile_y,tile_x,i):
		pacman=self.entities[0]
		if i==0: #vertical_check_tile_up
			if pacman.pos_in_grid_x != ghost.pos_in_grid_x:
				return False
			if tile_y<=ghost.pos_in_grid_y<=pacman.pos_in_grid_y:
				return True
		if i==1: #vertical_check_tile_down
			if pacman.pos_in_grid_x != ghost.pos_in_grid_x:
				return False
			if pacman.pos_in_grid_y<=ghost.pos_in_grid_y<=tile_y:
				return True
		if i==2: #tile left
			if pacman.pos_in_grid_y != ghost.pos_in_grid_y:
				return False
			if tile_x<=ghost.pos_in_grid_x<=pacman.pos_in_grid_x:
				return True
		if i==3: #tile right
			if pacman.pos_in_grid_y != ghost.pos_in_grid_y:
				return False
			if pacman.pos_in_grid_x<=ghost.pos_in_grid_x<=tile_x:
				return True
		return False

	def am_i_in_sandwitch(self):
		pacman=self.entities[ENTITIES.PACMAN.value]
		red=self.entities[ENTITIES.RED.value]
		pink=self.entities[ENTITIES.PINK.value]
		slice_of_bread=0	
		if self.possibilities[0]==0:
			if red.pos_in_grid_y>pacman.pos_in_grid_y or pink.pos_in_grid_y>pacman.pos_in_grid_y:
				slice_of_bread+=1
		if self.possibilities[1]==0:
			if red.pos_in_grid_y<pacman.pos_in_grid_y or pink.pos_in_grid_y<pacman.pos_in_grid_y:
				slice_of_bread+=1
		if self.possibilities[2]==0:
			if red.pos_in_grid_x>pacman.pos_in_grid_x or pink.pos_in_grid_x>pacman.pos_in_grid_x:
				slice_of_bread+=1
		if self.possibilities[3]==0:
			if red.pos_in_grid_x<pacman.pos_in_grid_x or pink.pos_in_grid_x<pacman.pos_in_grid_x:
				slice_of_bread+=1
		
		return slice_of_bread>1

	
 
	def check_game_over(self):
		pacman=self.entities[ENTITIES.PACMAN.value]
		red=self.entities[ENTITIES.RED.value]
		pink=self.entities[ENTITIES.PINK.value]
		self.is_game_over= (pacman.pos_in_grid_y == red.pos_in_grid_y and pacman.pos_in_grid_x == red.pos_in_grid_x) or (pacman.pos_in_grid_y == pink.pos_in_grid_y and pacman.pos_in_grid_x == pink.pos_in_grid_x)
	
def main():

	game= Game()

	while game.quit == False:
		check_for_events(game)
		if not game.is_running:
			continue
		keys_pressed = pygame.key.get_pressed()
		
		game.graphics.update_time(game.frame_iteration/60)
		action=check_keyboard() 
		game.get_closest_safe_exit()
		if game.is_game_over:
			game.reset()
		game.play_step(action) 
		game.play_ghost()

		if game.is_game_over:
			game.reset()

def check_for_events(game):
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game.quit = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_p: #if P is pressed, toggle pause
					game.is_running=not game.is_running
				if event.key == pygame.K_l: #if M is pressed, toggle debug
					game.debug=not game.debug
				if event.key == pygame.K_m:
					if pygame.mixer.music.get_volume() != 0.0:
						pygame.mixer.music.set_volume(0.0)
					else:
						pygame.mixer.music.set_volume(0.05)
				
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
