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
	#print(next_action)
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
		#print(result)
		return ([y, x] == turning_points).all(1).any()
 


class Game():
	def __init__(self, w=WIDTH, h=HEIGHT):
		self.w=w
		self.h=h
		self.frame_iteration = 0
		self.game_started= False
		self.graphics = gp.PacGraphic(w,h) #questa classe gestisce tutto cio' che e' grafico.
		self.graphics.FPS=60 #MAX FPS
		#0=clear_path,2=wall,1=coin,3=invalid
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0],[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3],[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3],[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2],[2,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2],[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2],[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.memory=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],[2,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,2],[2,2,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,2,2],[3,3,3,3,3,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,2,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,2],[2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],[2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],[2,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,2],[2,0,2,2,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,2],[2,0,2,2,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.grid[14,5]=0
		self.grid[14,22]=0
		#initialize entities
		self.entities = []
		self.init_entities()
		self.graphics.get_entities(self.entities)
		self.n_games=0
		self.s= solver(self.grid)
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
		#self.set_powerups()
		self.memory=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],[2,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,2],[2,2,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,2,2],[3,3,3,3,3,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,2,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3],[3,3,3,3,3,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,3,3,3,3,3],[2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],[2,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,2],[2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],[2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],[2,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,2],[2,0,2,2,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,2],[2,0,2,2,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,2],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		
		self.score=0
		self.graphics.reset()
		self.graphics.get_grid(self.grid)
		self.debug=False
		self.is_running=True
		self.is_game_over=False
		self.possibilities=[1,1,1,1]
		#self.in_corner=[0,0,0,0]
		self.red_in_corner=[0,0,0,0]
		self.pink_in_corner=[0,0,0,0]
		self.can_go_in_there_before_ghost()
	def set_powerups(self):
			self.grid[3,1]=-1
			self.grid[3,26]=-1
			self.grid[23,1]=-1
			self.grid[23,26]=-1


	def init_entities(self):
		pacman=Pacman(os.path.join('Assets', 'pac-tmp.png'),name="pacman")
		x,y=self.graphics.grid_to_window(row=23,col=12)
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
		x,y=self.graphics.grid_to_window(row=11,col=12)
		#offsettino_x=15#//2 #29/2
		#offsettino_y=16#//2 #33/2
		red.default_x=x#+offsettino_x
		red.default_y=y+48#36+offsettino_y
		red.set_rect(red.default_x,red.default_y,rect_dim,rect_dim)
		red.set_pos_in_grid()
		self.entities.append(red)
		#PINK
		pink=PinkGhost(os.path.join('Assets', 'pink-tmp.png'),self.grid,name="pinky")
		x,y=self.graphics.grid_to_window(row=11,col=15)
		pink.default_x=x
		pink.default_y=y+48
		pink.set_rect(pink.default_x,pink.default_y,rect_dim,rect_dim)
		pink.set_pos_in_grid()
		self.entities.append(pink)

		pacman.reset_invincibility()
	def am_i_regretting(self,pacman,next_action):
		#if pacman.old_action==Actions.HALT and next_action==Actions.HALT:
		#	return 1
		#se prima fa una wrong action e poi una azione legittima non dovrebbe essere punito come se facesse avanti indietro
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
		#return not self.can_move(next_action,pacman)
	def get_ghost_distance(self): #non usare
		pacman=self.entities[0]
		red=self.entities[1]
		pink=self.entities[2]
		py=pacman.pos_in_grid_y
		px=pacman.pos_in_grid_x
		ry=red.pos_in_grid_y
		rx=red.pos_in_grid_x
		pinky=pink.pos_in_grid_y
		pinkx=pink.pos_in_grid_x
		self.red_dist=float_sqrt(pow(abs(py-ry),2)+pow(abs(px-rx),2))#round(float_sqrt(pow(abs(py-ry),2)+pow(abs(px-rx),2)))
		self.pink_dist=float_sqrt(pow(abs(py-ry),2)+pow(abs(px-rx),2))#round(float_sqrt(pow(abs(py-pinky),2)+pow(abs(px-pinkx),2)))
	def can_go_in_there_before_ghost(self):
		pacman=self.entities[0]
		red=self.entities[1]
		pink=self.entities[2]
		py=pacman.pos_in_grid_y
		px=pacman.pos_in_grid_x

		
		#possible_paths=self.is_ghost_in_the_corner(ghost,pacman)
		#result=[]
		#for index,direction in enumerate(possible_paths):
		#	if direction==0:
		#		result.append(1)
		#	else:
			#calcola se distanza pacman-incrocio > ghost-incrocio
			#get incrocio
		self.possibilities=[1,1,1,1]
		self.red_in_corner=[0,0,0,0]
		self.pink_in_corner=[0,0,0,0]
		#i=0
		bonus=self.graphics.frame_iteration-self.graphics.old_iter
		four_direction=self.where_entity_is_looking(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
		for ghost_index,ghost in enumerate([red,pink]):
			gy=ghost.pos_in_grid_y
			gx=ghost.pos_in_grid_x
			tmp=self.is_ghost_in_the_corner(ghost,pacman)
			g_dist=ghost.distance_from_pacman
			#bigger_y=compare_int(red.pos_in_grid_y,pink.pos_in_grid_y)
			#bigger_x=compare_int(red.pos_in_grid_x,pink.pos_in_grid_x)
			# gf=0
			# if ghost.facing==FACING.NORTH:
			# 	gf=0
			# if ghost.facing==FACING.SOUTH:
			# 	gf=1
			# if ghost.facing==FACING.WEST:
			# 	gf=2
			# if ghost.facing==FACING.EAST:
			# 	gf=3
			#ghost_top=compare_int(py,gy)
			#ghost_left=compare_int(gx,px)
			danger_y,danger_x,facing=self.check_ghost_is_coming(ghost)
			for index in range(4): 
				if tmp[index]: #prevent ovveride positive in_corner by 2nd ghost 
					if ghost_index==0:
						self.red_in_corner[index]=1
					else:
						self.pink_in_corner[index]=1
				if ((four_direction[index][0],four_direction[index][1])==(pacman.pos_in_grid_y,pacman.pos_in_grid_x)):
						self.possibilities[index]=0
						continue
				if not danger_x and not danger_y: #se non si rischia continua
					continue
				if 	(index<2 and danger_y): #se si rischia sull'asse y
						p_dist=abs(py-four_direction[index][0])+2 #2
						g_dist=abs(gy-four_direction[index][0])
						if g_dist<=p_dist:
							self.possibilities[index]=0
							continue
				if 	(index>=2 and danger_x): #se si rischia sull'asse x
					p_dist=abs(px-four_direction[index][1])+2 #2
					g_dist=abs(gx-four_direction[index][1])
					if g_dist<=p_dist:
						self.possibilities[index]=0
						continue
			

		for i in range(4): #MOLTO IMPORTANTE
			self.possibilities[i]=int(self.possibilities[i] and not (self.red_in_corner[i] or  self.pink_in_corner[i]))


				#casi senza ombra di dubbio
				# if index==0  and px == gx and compare_int(gy,py)==1: #if up
				# 	continue
				# if index==1 and px == gx and compare_int(py,gy)==1: #if down
				# 	continue
				# if index==2 and py == gy and compare_int(gx,px)==1: #if sx
				# 	continue
				# if index==3 and py == gy and compare_int(px,gx)==1: #if dx
				# 	continue
				#if index==0  and compare_int(gy,py)>=0: #if up
				#	continue
				#if index==1 and compare_int(py,gy)>=0: #if down
				#	continue
				#if index==2  and compare_int(gx,px)>=0: #if sx
				#	continue
				#if index==3 and compare_int(px,gx)>=0: #if dx
				#	continue
				
				#print(index,p_dist,g_dist)
				
				#if (p_dist-1)-g_dist>=0:
				#	self.possibilities[index]=0
				
				#if index<2: #se vogliamo muoverci up or down
					#if ghost.name=="blinky":
					#	print(g_dist,1+abs(four_direction[index][0]-py))
					
				#	if p_dist-g_dist>=0:
				#		self.possibilities[index]=0
				#if index>=2: #se vogliamo muoverci left or right
					#if ghost.name=="blinky":
					#	print(g_dist,1+abs(four_direction[index][1]-px))
				#if abs(four_direction[index][1]-px)-(g_dist)+4>0:
				#		self.possibilities[index]=0


				#self.graphics.highlight_specific_cell(four_direction[index][0],four_direction[index][1])
				#i=i+1

				#p_dist=float_sqrt(pow(abs(py-four_direction[index][0]),2)+pow(abs(px-four_direction[index][1]),2))
				#g_dist=float_sqrt(pow(abs(gy-four_direction[index][0]),2)+pow(abs(gx-four_direction[index][1]),2))
				#print(p_dist)

				#if index >2: #lavoriamo sulle y
					#p_dist=abs(py-four_direction[index][0])
					#g_dist=abs(gy-four_direction[index][0])
				#else:
					#p_dist=abs(px-four_direction[index][1])
					#g_dist=abs(gx-four_direction[index][1])
				#p_dist=self.s.get_path_lenght(four_direction[index][0],four_direction[index][1],pacman.pos_in_grid_y,pacman.pos_in_grid_x)
				#g_dist=self.s.get_path_lenght(four_direction[index][0],four_direction[index][1],ghost.pos_in_grid_y,ghost.pos_in_grid_x)
				#supponiamo pacman sia veloce x2 rispetto a ghost
				#if (p_dist)>=(g_dist+bonus) or ((four_direction[index][0],four_direction[index][1])==(pacman.pos_in_grid_y,pacman.pos_in_grid_x)):
				#	self.possibilities[index]=0 #if (p_dist)<(g_dist) else 0 #and in_corner[index]==0 else 0
				
		#print(i)
		#result.append(1 if p_dist<g_dist else 0)
		#return result
		#print(bonus)
		#print(self.possibilities)
		#print(self.in_corner)
		#print("---")
		#for index in range(4):
			#if self.possibilities[index]==0:
				#self.graphics.highlight_specific_cell(four_direction[index][0],four_direction[index][1])
			#if self.red_in_corner[index] or self.pink_in_corner[index]:
			#	ghost_looking_at= self.where_entity_is_looking(ghost.pos_in_grid_y,ghost.pos_in_grid_x)
				#self.graphics.highlight_specific_cell(*ghost_looking_at[ghost.facing.value])
	def is_ghost_in_the_corner(self,ghost,pacman):
		#restituisce 1 array boolean [N,S,W,O] se 0=puoi andare lì senza che ghost sia in agguato
			pacman_looking_at= self.where_entity_is_looking(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
			ghost_looking_at= self.where_entity_is_looking(ghost.pos_in_grid_y,ghost.pos_in_grid_x)
			#print(ghost_looking_at)
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
				#print(array)
				if index<2 and ghost.pos_in_grid_x==pacman.pos_in_grid_x:
					continue
				if index>=2 and ghost.pos_in_grid_y==pacman.pos_in_grid_y:
					continue
				for index in array:
					if not (pacman_looking_at[index][0]==pacman.pos_in_grid_y and pacman_looking_at[index][1]==pacman.pos_in_grid_x):
						result[index]=1
			#print(result)
			return result
			
			
	def is_in_turning_point(self,y,x):
		turning_points=np.array([[1,1],[1,6],[1,12],[1,15],[1,21],[1,26],[5,1],[5,6],[5,9],[5,12],[5,15],[5,18],[5,21],[5,26],[8,1],[8,6],[8,9],[8,12],[8,15],[8,18],[8,21],[8,26],[11,9],[11,12],[11,15],[11,18],[14,6],[14,9],[14,18],[14,21],[17,9],[17,18],[20,1],[20,6],[20,9],[20,12],[20,15],[20,18],[20,21],[20,26],[23,1],[23,3],[23,6],[23,9],[23,12],[23,15],[23,18],[23,21],[23,24],[23,26],[26,1],[26,3],[26,6],[26,9],[26,12],[26,15],[26,18],[26,21],[26,24],[26,26],[29,1],[29,12],[29,15],[29,26]])
		return ([y, x] == turning_points).all(1).any()		

	#inutile funzione
	def wall_is_there(self,y,x):
		if y<0 or y>30 or x<0 or x>27:
			return -1
		if self.grid[y][x]==2:
			return 1
		else:
			return 0


	def where_entity_is_looking(self,y,x):
		#ritorna 4 coppie di valori [y,x] per ogni direzione cardinale. la coppia
		#corrisponde al punto di intersezione + vicino
		#return [[Y,X],[Y,X],[Y,X][Y,X]]
		result = []
		ey=y
		ex=x

		i=1
		#NORTH
		while self.grid[ey-i,ex]!=2:
			if self.is_in_turning_point(ey-i,ex):
				i+=1 #per bilanciare il +1 del muro
				break
			i+=1
		result.append([ey-i+1,ex])
		i=1
		#SOUTH
		while self.grid[ey+i,ex]!=2:
			if self.is_in_turning_point(ey+i,ex):
				i+=1 #per bilanciare il -1 del muro
				break
			i+=1
		result.append([ey+i-1,ex])
		#WEST
		i=1
		while self.grid[ey,ex-i]!=2:
			if ex-i==0: #if tunnel
				ex=20
				i=0
				break	
			if self.is_in_turning_point(ey,ex-i):
				i+=1 #per bilanciare il +1 del muro
				break
			i+=1
		result.append([ey,ex-i+1])
		i=1
		ex=x
		if ex==27:
			ex=0
		#EAST
		while self.grid[ey,ex+i]!=2:
			if ex+i==27: #if tunnel
				ex=7
				i=0
				break
			if self.is_in_turning_point(ey,ex+i):
				i+=1 #per bilanciare il +1 del muro
				break
			i+=1
		result.append([ey,ex+i-1])

		return np.array(result)

	

	def look_for_line(self,y,x,target_y,target_x):
		action=None
		found=[0,0]
		if target_y<y:
			action=Actions.UP
		if target_y>y:
			action=Actions.DOWN
		if target_x<x:
			action=Actions.LEFT
		else:
			action=Actions.RIGHT
		
		if action==Actions.UP:
			while( (y,x)!=(target_y,target_x) ):
				if self.grid[y][x]==1:
					found=[y,x]
					break
				y+=-1
		if action==Actions.DOWN:
			while( (y,x)!=(target_y,target_x) ):
				if self.grid[y][x]==1:
					found=[y,x]
					break
				y+=+1
		if action==Actions.LEFT:
			while( (y,x)!=(target_y,target_x) ):
				if self.grid[y][x]==1:
					found=[y,x]
					break
				x+=-1
		
		return found
			

	def get_closest_safe_exit(self):
		py=self.entities[0].pos_in_grid_y
		px=self.entities[0].pos_in_grid_x
		safe_points=np.array([[1,6],[1,21],[5,1],[5,6],[5,9],[5,12],[5,15],[5,18],[5,21],[8,6],[8,21],[11,12],[11,15],[14,6],[14,9],[14,18],[14,21],[17,9],[17,18],[20,6],[20,9],[20,18],[20,21],[23,6],[23,9],[23,12],[23,15],[23,18],[23,21],[26,3],[26,24],[29,12],[29,15]])
		#coords=self.where_entity_is_looking(py,px)

		#cheese_coords=np.array(np.where(self.grid==1)).T #get all coords where there is cheese
		closest_exit=[0,0,999]
		exits = np.array([])
		for coords in safe_points:
			dist=float_sqrt(pow(abs(py-coords[0]),2)+pow(abs(px-coords[1]),2))
			exits=np.append(exits, np.array([[coords[0],coords[1],dist]]))
		
		exits=exits.reshape(33,3)
		exits=exits[exits[:, 2].argsort()]
		#print(exits[:4])
		dghost=[self.entities[1].distance_from_pacman,self.entities[2].distance_from_pacman]
		#print(dghost)
		for i in range(8):
			next_tile_to_get_there,exits[i][2]=self.s.get_path(py,px,int(exits[i][0]),int(exits[i][1]))
			if next_tile_to_get_there==(-1,-1): #la safe exit è dove pacman si trova
				self.exit_top=0
				self.exit_left=0
				return
			index_of_possibilities=-1
			for index,mod in enumerate([[-1,0],[+1,0],[0,-1],[0,+1]]): #capisci se deve andare up,down,left,right to get to the exit
				if ((py+mod[0]),(px+mod[1]))==next_tile_to_get_there:
					index_of_possibilities=index
					break

			#print(next_tile_to_get_there)
			#print(exits[i])
			
			if  dghost[0]-exits[i][2]>0 and dghost[0]-exits[i][2]>0:
				if self.possibilities[index_of_possibilities] :
				#print(py,exits[i][0])
				#print(px,exits[i][1])
					self.exit_top=compare_int(py,exits[i][0])
					self.exit_left=compare_int(px,exits[i][1])
				#print(exits[i][0],exits[i][1])
				#print(self.exit_top,self.exit_left)
				 #questa safe exit è raggiungibile
				return
			#else:
				
				#print(i)
				#print(i,exits[i])
				#print("bloccata da ghost")
		
		#non esiste una exit raggiungibile senza morire
		self.exit_top=-2
		self.exit_left=-2
		#input()
			#if dist < closest_exit[2]:
			#	closest_exit=[coords[1],coords[0],dist]
		#print(closest_exit[1],closest_exit[0])
		
		#self.exit_top=compare_int(py,closest_exit[0])
		#self.exit_left=compare_int(px,closest_exit[1])
	def get_closest_cheese(self): #non e' perfetto ma amen
		if self.check_game_won():
			return 0,0,0
		#parte da pacman. controlla se a c'è un formaggio su,poi giù, sx e dx. se non c'è parte la ricorsione
		pacman=self.entities[ENTITIES.PACMAN.value]
		y=pacman.pos_in_grid_y
		x=pacman.pos_in_grid_x
		#cheese_y=-1
		#cheese_x=-1
		#self.BEST=np.array([-1,-1,999])
		self.BEST=[-1,-1,999]
		#print(self.BEST[2])
		#np.empty((0, 3),dtype='int16')
		#self.best_results=np.empty((0, 3),dtype='int16')
		self._recursive_cheese(y,x,0,(pacman.facing.value)+1)
		#self.compare_distance_of_all_cheese()
		#self.best_results.sort(key=lambda x: x[2])
		#print(self.best_results)
		#sorted(self.best_results, key=lambda x:x[2])
		#print("________________")
		#print(self.best_results) 
		#print(len(self.best_results))
		#if len(self.best_results)<1: #nel caso si rompa qualcosa
		#	print("rotto")
		#	self.best_results=[[11,13,99]]
		#print(self.BEST)	 
		cheese_y=self.BEST[0]
		cheese_x=self.BEST[1]
		cheese_dist=self.BEST[2]
		cheese_top=compare_int(y,cheese_y)
		cheese_left=compare_int(x,cheese_x)

		return cheese_top,cheese_left,cheese_dist
		#print(f"({cheese_y},{cheese_x}),dist: {best_result[2]}")
		#self.cheese_dist=p_dist=self.s.get_path_lenght(cheese_y,cheese_x,pacman.pos_in_grid_y,pacman.pos_in_grid_x)
		#print(self.cheese_dist)
		#print(f"({cheese_y},{cheese_x}), dist: {self.cheese_dist}")
		#return cheese_top,cheese_left
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

		#if np.count_nonzero(self.grid == 1) < 20:
		#return self.compare_distance_of_all_cheese()
		#print(dist)
		#print(dist,best_result[2])
		#print(len(self.best_results))
		#if len(self.best_results)>=min(1,np.count_nonzero(self.grid == 1)): 
		#	return
		if dist>35:
			return self.compare_distance_of_all_cheese()
			#print("aiuto non so dove patthare")
			#self.BEST=[17,13,1]
			#return
			#if not self.best_results:
			#	print("sono un pesce")
				#serve???? secondo me non e' quello ma sono tanti spazi bianchi
		#	return
		#	return

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
			#if dist<best_result[2]:
				#print("trovato")
				#best_result=[next_y,next_x,dist+1]
			#print(dist)
			
			#np.concatenate(self.best_results, np.array([[next_y,next_x,dist+1]]))
			#self.best_results=np.append(self.best_results, np.array([[next_y,next_x,dist+1]]))
			
			#print(self.best_results)
			#self.best_results.append([next_y,next_x,dist+1])
			if dist+1<self.BEST[2]:
				self.BEST=[next_y,next_x,dist+1]
			return
			#print(f"({next_y},{next_x}),dist: {dist}")
				#return best_result[:]
			#result=[next_y,next_x]
			#return result[:]
		next_y=y+1 #down
		if prev_direction!= 1:
			found2=self._get_neightbour_cheese(next_y,next_x)
		if found2==1:
			#if dist<best_result[2]:
				#print("trovato")
			#print(dist)	
			#print(f"({next_y},{next_x}),dist: {dist}")
			#self.best_results.append([next_y,next_x,dist+1])
			if dist+1<self.BEST[2]:
				self.BEST=[next_y,next_x,dist+1]
			#self.best_results=np.append(self.best_results, np.array([[next_y,next_x,dist+1]]))
			return
				#result=[next_y,next_x]
				#return result[:]
		next_y=y
		next_x=x-1 #left
		if prev_direction !=4:
			found3=self._get_neightbour_cheese(next_y,next_x)
		if found3==1:
			#print(dist)
			#if dist<best_result[2]:
				#print("trovato")
			#print(f"({next_y},{next_x}),dist: {dist}")
			#self.best_results.append([next_y,next_x,dist+1])
			#self.best_results=np.append(self.best_results, np.array([[next_y,next_x,dist+1]]))
			if dist+1<self.BEST[2]:
				self.BEST=[next_y,next_x,dist+1]
			return
			#result=[next_y,next_x]
			#return result[:]
		next_x=x+1 #right
		if prev_direction !=3:
			found4=self._get_neightbour_cheese(next_y,next_x)
		if found4==1:
			#print(dist)
			#if dist<best_result[2]:
				#print("trovato")
			#print(f"({next_y},{next_x}),dist: {dist}")
			#self.best_results.append([next_y,next_x,dist+1])
			if dist+1<self.BEST[2]:
				self.BEST=[next_y,next_x,dist+1]
			#self.best_results=np.append(self.best_results, np.array([[next_y,next_x,dist+1]]))
			return
			#result=[next_y,next_x]
			#return result[:]
			
		#print("non ho trovato niente")
		#print(found1,found2,found3,found4)
		#if 1 in [found1,found2,found3,found4]:
		#	return
				#if 1 in [found1,found2,found3,found4]:
		#	return
		#sorted(self.best_results, key=lambda x:x[2])
		#self.best_results= self.best_results[self.best_results[:, 2].argsort()]
		#print(self.best_results[0][2])
		if found1 == 0:
			if dist+1<self.BEST[2]:
				self._recursive_cheese(y-1,x,dist+1,1)
			
			#if tmp and tmp[2]<best[2]:
			#	best=tmp
		if found2 == 0:
			if dist+1<self.BEST[2]:
				self._recursive_cheese(y+1,x,dist+1,2)
			#if tmp and tmp[2]<best[2]:
			#	best=tmp
		if found3 == 0:
			if dist+1<self.BEST[2]:
				self._recursive_cheese(y,x-1,dist+1,3)
			#if tmp and tmp[2]<best[2]:
			#	best=tmp

		if found4 == 0:
			if dist+1<self.BEST[2]:
				self._recursive_cheese(y,x+1,dist+1,4)
			#if tmp and tmp[2]<best[2]:
			#	best=tmp
		#print(best)
		#return best[:]
		#return
		
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
	
	def get_neightbour(self,neightbour_y,neightbour_x): #gli ho ordinati così affinché l'ai faccia il ragionamento: grande->meglio
		if self.grid[neightbour_y,neightbour_x]>=2:
			return 0
		
		if self.grid[neightbour_y,neightbour_x]==0:
			return 1
		if self.grid[neightbour_y,neightbour_x]==1:
			return 2
		if self.grid[neightbour_y,neightbour_x]==-1:
			return 3
	
	def check_danger(self,ghost): #rotto
		pacman=self.entities[0]
		py=pacman.pos_in_grid_y
		px=pacman.pos_in_grid_x
		ey=ghost.pos_in_grid_y
		ex=ghost.pos_in_grid_x
		four_direction=self.where_entity_is_looking(ey,ex)
		danger_y=0
		danger_x=0
		for index,turning_point_looked in enumerate(four_direction):
			if turning_point_looked[0]==py and turning_point_looked[1]==px:
				if index<2:
					danger_y=1
				else:
					danger_x=1
		return danger_y,danger_x
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
		return y,x, entity.facing
	def check_ghost_is_coming3(self,entity): 
		pacman=self.entities[0]
		height=65
		width=16 
		py=pacman.pos_in_grid_y
		px=pacman.pos_in_grid_x
		ey=entity.pos_in_grid_y
		ex=entity.pos_in_grid_x
		entity_long_rect_y= pygame.Rect(entity.rect.x-pacman.rect.height/2,entity.rect.y-height+entity.rect.width/2,width,height*2)
		pacman_long_rect_y= pygame.Rect(pacman.rect.x-entity.rect.height/2,pacman.rect.y-height+pacman.rect.width/2,width,height*2)
		entity_long_rect_x= pygame.Rect(entity.rect.x-height+entity.rect.width/2,entity.rect.y-entity.rect.height/2,height*2,width)
		pacman_long_rect_x= pygame.Rect(pacman.rect.x-height+pacman.rect.width/2,pacman.rect.y-pacman.rect.height/2,height*2,width)
		y=0
		x=0
		if entity_long_rect_y.colliderect(pacman_long_rect_y):
			#pygame.draw.rect(self.graphics.WIN,(200,0,0),entity_long_rect_y)
			#pygame.draw.rect(self.graphics.WIN,(255,0,0),pacman_long_rect_y)
			#pygame.display.update()
			if entity.facing==FACING.SOUTH and py > ey:
				# #return True
				y=1
				# #print("kek s")
			if entity.facing==FACING.NORTH and py < ey:
				# #return True
				y=1
				# #print("kek n")
		if entity_long_rect_x.colliderect(pacman_long_rect_x):
			#pygame.draw.rect(self.graphics.WIN,(0, 0, 255),entity_long_rect_x)
			#pygame.draw.rect(self.graphics.WIN,(0,255,0),pacman_long_rect_x)
			#pygame.display.update()
			if entity.facing==FACING.WEST and px < ex:
				# #return True
				x=1
				# #print("kek w")
			if entity.facing==FACING.EAST and px > ex:
				# #return True
				x=1
				# #print("kek e")
		return y,x, entity.facing
	def check_ghost_is_coming2(self,entity): #check warning
		pacman=self.entities[0]
		long=160
		short=30
		py=pacman.pos_in_grid_y
		px=pacman.pos_in_grid_x
		ey=entity.pos_in_grid_y
		ex=entity.pos_in_grid_x
		#entity_long_rect_y= pygame.Rect(entity.rect.x-pacman.rect.height/2,entity.rect.y-height+entity.rect.width/2,width,height*2)
		#pacman_long_rect_y= pygame.Rect(pacman.rect.x-entity.rect.height/2,pacman.rect.y-height+pacman.rect.width/2,width,height*2)
		#entity_long_rect_x= pygame.Rect(entity.rect.x-height+entity.rect.width/2,entity.rect.y-entity.rect.height-width+20,height*2,width*3)
		#pacman_long_rect_x= pygame.Rect(pacman.rect.x-height+pacman.rect.width/2,pacman.rect.y-pacman.rect.height-width+20,height*2,width*3)
		pacman_long_rect= pygame.Rect(pacman.rect.x,pacman.rect.y,30,30)
		#pacman_long_rect_x= pygame.Rect(pacman.rect.x,pacman.rect.y,30,30)
		if pacman.facing.value<2:
			entity_long_rect=pygame.Rect(entity.rect.x-short/2,entity.rect.y-long/2-short,short*2,long*2)
		else:
			entity_long_rect=pygame.Rect(entity.rect.x-long/2-short,entity.rect.y-short,long*2,short*2)
		y=0
		x=0
		if entity_long_rect.colliderect(pacman_long_rect):
			#if entity.name=="blinky":
			#pygame.draw.rect(self.graphics.WIN,(200,0,0),entity_long_rect)
			#pygame.draw.rect(self.graphics.WIN,(0,0,0),pacman_long_rect)
			#pygame.display.update()
			return entity.facing.value
		return -1
		#if entity_long_rect_y.colliderect(pacman_long_rect):
			#pygame.draw.rect(self.graphics.WIN,(200,0,0),entity_long_rect_y)
			#pygame.draw.rect(self.graphics.WIN,(0,0,0),pacman_long_rect)
			#pygame.display.update()
			#if entity.facing==FACING.SOUTH and py > ey:
				# #return True
				#y=1
				# #print("kek s")
			#if entity.facing==FACING.NORTH and py < ey:
				# #return True
				#y=1
				# #print("kek n")
		#if entity_long_rect_x.colliderect(pacman_long_rect):
			#pygame.draw.rect(self.graphics.WIN,(0, 0, 255),entity_long_rect_x)
			#pygame.draw.rect(self.graphics.WIN,(0,0,0),pacman_long_rect)
			#pygame.display.update()
		#	if entity.facing==FACING.WEST and px < ex:
				# #return True
		#		x=1
				# #print("kek w")
		#	if entity.facing==FACING.EAST and px > ex:
				# #return True
		#		x=1
				# #print("kek e")
		#return y,x, entity.facing
	
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
	def move_entity(self,entity,action): #serve giusto per muoverlo a livello di pixels
		rect=entity.rect
		VEL=entity.VEL
		cheese_eaten=False
		ex,ey=entity.window_to_grid()
		ex,ey=self.graphics.grid_to_window(ey,ex)
		entity.old_action=action
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
			if action!=Actions.HALT:
				self.last_meaninful_action=0 if action==Actions.UP else 1 if action==Actions.DOWN else 2 if action==Actions.LEFT else 3 if action==Actions.RIGHT else -1 
			#print(self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x])
			if self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x]==1:
				cheese_eaten=True
				self.number_of_cheeese_eaten+=1
			if self.grid[entity.pos_in_grid_y][entity.pos_in_grid_x]==-1:
				#entity.invincible=1
				cheese_eaten=True #lo metto solo per il reward, anche se non e' un formaggio
				#entity.invincibility_timestamp=self.graphics.frame_iteration
				#entity.set_invincibility_sprite()
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
			return True
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
		#if next_y==14: 
		#	if next_x==-1:
			#	return True
				#next_x=9
				#print("tippo")
		#	if next_x==28:
		#		return True
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

	def play_ghost(self):
		self.graphics.frame_iteration+=1
		#print(self.graphics.frame_iteration,self.graphics.old_iter)
		#sicurezza= distanza fantasma-pacman? e punisco quando la sicurezza diminuisce 
		#print(action)
		pacman=self.entities[ENTITIES.PACMAN.value]
		#if self.graphics.timer <2.5:
			#return #il timer lo abilito nella release, mentre sviluppo e' una perdita di tempo
		#	pass 
		
		if self.graphics.frame_iteration>self.graphics.old_iter+6: #2
			self.graphics.old_iter=self.graphics.frame_iteration
			#print("muovo")
			for entity in self.entities: #for each ghost
				if entity.name == "pacman":
					continue
				#if not is_in_turning_point(entity):
				#	ghost_action=entity.old_action
				#else:
				dy,dx=entity.get_new_path(pacman)
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
		self.check_game_over()

	def play_step(self,action):
		reward=0
		self.check_game_over()
	
		pacman=self.entities[ENTITIES.PACMAN.value]
		red=self.entities[1]
		pink=self.entities[2]
		if self.is_game_over:
				reward=-4000
				self.n_games+=1
				return reward, self.is_game_over, self.score
		if self.graphics.timer <2.5:
			#return #il timer lo abilito nella release, mentre sviluppo e' una perdita di tempo
			pass 

		#game_over=0
		#log=""
		#print(self.possibilities)

		#if not self.can_move(action,pacman):
		 	#print("wrong action")
		#reward+=-5
		self.get_closest_safe_exit()
		self.stuck=int(self.am_i_regretting(pacman,action))# or not self.can_move(action,pacman)) #or action==Actions.HALT)#: #se stai fermo 
		turbo_stuck=self.stuck or action == Actions.HALT or not self.can_move(action,pacman)

		if not self.can_move(action,pacman):
			reward+=-150

		# toppest_ghost_y=min(red.pos_in_grid_y,pink.pos_in_grid_y)
		# leftest_ghost_x=min(red.pos_in_grid_x,pink.pos_in_grid_x)

		# if action==Actions.UP:
		# 	if toppest_ghost_y<pacman.pos_in_grid_y:
		# 		reward+=-50
		# 	if toppest_ghost_y>pacman.pos_in_grid_y:
		# 		reward+=+50
		# if action==Actions.DOWN:
		# 	if toppest_ghost_y>pacman.pos_in_grid_y:
		# 		reward+=-50
		# 	if toppest_ghost_y<pacman.pos_in_grid_y:
		# 		reward+=+50
		# if action==Actions.LEFT:
		# 	if leftest_ghost_x<pacman.pos_in_grid_x:
		# 		reward+=-50
		# 	if leftest_ghost_x>pacman.pos_in_grid_x:
		# 		reward+=+50
		# if action==Actions.RIGHT:
		# 	if leftest_ghost_x>pacman.pos_in_grid_x:
		# 		reward+=-50
		# 	if leftest_ghost_x<pacman.pos_in_grid_x:
		# 		reward+=+50
		self.can_go_in_there_before_ghost()
		self.safe_exit=do_i_have_a_third_exit(pacman,action)
		if self.stuck: #and not self.safe_exit:
			reward+=-1200
			#print("stuck")
		if not (self.possibilities[0]) and action in [Actions.UP,Actions.HALT]:
			if action==Actions.HALT:
				if not self.safe_exit:
					reward+=-200
			else:
				reward+=-400
		#	if self.in_corner[0]:
		#		reward+=-80
		if not (self.possibilities[1]) and action in [Actions.DOWN,Actions.HALT]:
			if action==Actions.HALT:
				if not self.safe_exit:
					reward+=-200
			else:
				reward+=-400
		#	if self.in_corner[1]:
		#		reward+=-80
		if not (self.possibilities[2]) and action in [Actions.LEFT,Actions.HALT]:
			if action==Actions.HALT:
				if not self.safe_exit:
					reward+=-200
			else:
				reward+=-400
		#	if self.in_corner[2]:
		#		reward+=-80
		if not (self.possibilities[3]) and action in [Actions.RIGHT,Actions.HALT]:
			if action==Actions.HALT:
				if not self.safe_exit:
					reward+=-200
			else:
				reward+=-400
		
		#else:
		#	if action==Actions.HALT:
		#		if not self.safe_exit:
		#			reward+=-100
		#		else:
		#			reward+=100
		#	if self.in_corner[3]:
		#		reward+=-80

		#if action in [Actions.UP]:#,Actions.HALT]:# or not self.can_move(action,pacman): 
		#	if not (self.possibilities[0]):#and self.possibilities[4]):
		#		reward+=-20
		#	if self.in_corner[0]:# and not self.safe_exit:
		#		reward+=-10
		#if action in [Actions.DOWN]:#,Actions.HALT]:# or not self.can_move(action,pacman): 
		#	if not (self.possibilities[1]):# and self.possibilities[5]):
		#		reward+=-20
		#	if self.in_corner[1]:# and not self.safe_exit:
		#		reward+=-10
		#if action in [Actions.LEFT]:#,Actions.HALT]: #or not self.can_move(action,pacman): 
		#	if not (self.possibilities[2]):# and self.possibilities[6]):
		#		reward+=-20
		#	if self.in_corner[2]:# and not self.safe_exit:
		#		reward+=-10
		#if action in [Actions.RIGHT]:#,Actions.HALT]:# or not self.can_move(action,pacman): 
		#	if not (self.possibilities[3]):# and self.possibilities[7]):
		#		reward+=-20
		#	if self.in_corner[3]:# and not self.safe_exit:
		#		reward+=-10
		#print("sono a: "+str(pacman.pos_in_grid_y)+","+str(pacman.pos_in_grid_x)+" e voglio andare " + str(action))
		#print("game: "+str(action))

		#old_cheese_dist=self.cheese_dist
		#print(self.possibilities)
		#if am_i_regretting(pacman,action):#aggiungere am_i_regretting e last action.
		
		#self.stuck=0
	

		#TODO FARE CLOSEST EXIT CON METODO RICORSIVO
		#self.stuck=1
			#print("stai bello am_i_regretting")
			#reward-=20
			#self.unsure=1

				#print("me la chillo safe")
		#	else:
		#		reward+=-50
				#print("sono cuckato e non al sicuro")
		#else:
			#self.unsure=0
		#if not self.can_move(action,pacman): #or self.stuck:
		#	reward+=-30

		#old_red_dist=red.distance_from_pacman
		#old_pink_dist=pink.distance_from_pacman
		cheese_eaten= self.move_entity(pacman,action)
		
		self.cheese_top,self.cheese_left,dist=self.get_closest_cheese()
		self.cheese_zone_y,self.cheese_zone_x=self.get_zone(self.cheese_left,self.cheese_top)
		self.pacman_zone_y,self.pacman_zone_x=self.get_zone(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
		
		self.red_getting_closer=int(red.distance_from_pacman < red.old_distance )
		self.pink_getting_closer=int(pink.distance_from_pacman < pink.old_distance )
		#self.get_ghost_distance()
		#self.safe_exit=do_i_have_a_third_exit(pacman)
		#if self.stuck:
		#	reward+=-150
		#double_danger_pass=(self.check_ghost_is_coming2(red) !=-1) and (self.check_ghost_is_coming2(pink) !=-1)
		int_count=0
		dodge_count=0
		self.red_distance_lvl=round(red.distance_from_pacman/3)
		self.pink_distance_lvl=round(pink.distance_from_pacman/3)
		dist_lvl= [self.red_distance_lvl,self.pink_distance_lvl]
	
		for index,ghost in enumerate([red,pink]):
			#print(ghost.distance_from_pacman)
		 	#danger_y,danger_x=self.check_danger(ghost)
			#danger_y,danger_x,facing=self.check_ghost_is_coming2(ghost)
			
			warning_facing=self.check_ghost_is_coming2(ghost)
			if warning_facing != -1: # in danger!
				reward+=-500
			else:
				reward+=100
			#if warning_facing != -1: # in danger!
			#	reward+=-50
			#else:
			#	reward+=10
			same_danger_axis=0
			if pacman.facing.value<2:
				same_danger_axis=abs(ghost.pos_in_grid_x - pacman.pos_in_grid_x)<=2 #1
				#double_danger_pass= double_danger_pass and (ghost.pos_in_grid_x != pacman.pos_in_grid_x)
			else:
				same_danger_axis=abs(ghost.pos_in_grid_y - pacman.pos_in_grid_y)<=2 #1
				#double_danger_pass= double_danger_pass and (ghost.pos_in_grid_y != pacman.pos_in_grid_y)
			inting= [ghost.facing.value,pacman.facing.value] in [[0,1],[1,0],[2,3],[3,2]] #controllare inting
			inting= inting and same_danger_axis

			if inting:	
				#print(dist_lvl)
				if dist_lvl[index]==0:
					reward+=-1000
				elif dist_lvl[index]>=2:
					reward+=dist_lvl[index]*20
				else:
					if not self.safe_exit:
						reward+=-(2-dist_lvl[index])*300
		#	ghost_getting_closer=ghost.distance_from_pacman < ghost.old_distance
			#inting= inting and ghost_getting_closer#same_danger_axis
		#	inting=ghost_getting_closer and same_danger_axis
			
		if warning_facing == -1: #if safe
			pass
			#if action==Actions.HALT and self.safe_exit:
			#	reward+=20
			#reward+=10 
		else: #if danger
			#print("fermo in pericolo")
			if inting: #or not self.can_move(action,pacman):
				reward+=-400
				#pass

				#int_count+=1
					#print("sto intando")
					
			else:
				pass
				#dodge_count+=1
				#reward+=80
				#print("scappo da danger")
		
		#print(dodge_count,int_count)
		#if int_count:
			#if dodge_count==0:
			#	#print("male")
			#	for i in range(int_count):
			#		reward+=-400
			#else:
			#	reward+=200
				#print("bene")
		
		#if dodge_count==0 and self.stuck:
		#	reward+=-200
		#else:
		#	if int_count:
		#		print("fake")
			# danger_y,danger_x,facing=self.check_ghost_is_coming(ghost)
			# if danger_y:
			# 		if(inting):
			# 			reward+=-150
			# 		elif self.stuck or not self.can_move:
			# 			reward+=-30
			# 		else:
			# 			reward+=120
			# 			print("scappo da danger rosso")
			# if danger_x:
			# 		reward+=-80
			# 		if(inting):
			# 			reward+=-70
			# 		elif self.stuck or not self.can_move:
			# 			reward+=-30
			# 		else:
			# 			reward+=120
			# 			print("scappo da danger pink")


		#print(self.red_getting_closer)
		#print(self.red_in_corner)
		# for i in range(4):
		# 	if self.red_in_corner[i]==1:
				
		# 		if self.red_getting_closer and not self.safe_exit:
		# 			reward+=-80
		# 		else: #si allontana
		# 			#print("è nel corner e mi allontano")
		# 			reward+=50
		# 	if self.pink_in_corner[i]==1:
		# 		if self.pink_getting_closer and not self.safe_exit:
		# 			reward+=-80
		# 		else: #si allontana
		# 			reward+=50

			
			#		reward+=-30
			#	elif action != Actions.HALT:
			#		reward+=+20
			#	else:
			#		reward+=-20					
			
		#old_corner=self.in_corner


		


		#if self.safe_exit:
		#	reward+=5
		#if self.grid[pacman.pos_in_grid_y][pacman.pos_in_grid_x]==0: #sempre btw
		#	if do_i_have_a_third_exit(pacman):
		#		self.safe_exit=1
		#		reward-=1
		#	else:
		#		reward-=5
			#self.safe_exit=0
		#	reward-=5
		#if self.have_i_been_here_before(action,pacman]):
			#reward-=5 #+pow(1.01,self.number_of_cheeese_eaten)
		#if old_cheese_dist<=self.cheese_dist:
		#	reward+=3
		self.sandwitch=self.am_i_in_sandwitch()
		#exit_top e left dovrebbero escludere le exit che sono bloccate dai fantasmi (guardare self.possibilities)
		#se il discorso della safe exit è troppo difficile da implementare a questo punto andare con tecnologia anti corner
		if self.sandwitch:
			if self.safe_exit:
				reward+=400
			# 	#print("si gode")
			else:	
				if self.exit_top==1 and action in [Actions.UP]:
					reward+=70
				elif self.exit_top==-1 and action in [Actions.DOWN]:
					reward+=70
				elif self.exit_left==1 and action in [Actions.LEFT]:
					reward+=70
				elif self.exit_left==-1 and action in [Actions.RIGHT]:
					reward+=70
				else:
					reward+=-1000
					#print("sono stronzo")

		if cheese_eaten:
			self.score+=10
			reward+=500 #+ pow(1.03,self.number_of_cheeese_eaten)
		else:
			#if self.pacman_zone_y==self.cheese_zone_y and  self.pacman_zone_x==self.cheese_zone_x:
			#	reward+=80
			if self.cheese_top and action==Actions.UP: #not in [Actions.DOWN,Actions.HALT]:
				reward+=40
			if not self.cheese_top and action==Actions.DOWN:#action not in [Actions.UP,Actions.HALT]:
				reward+=40
			if self.cheese_left and action==Actions.LEFT:#action not in [Actions.RIGHT,Actions.HALT]:
				reward+=40
			if not self.cheese_left and action==Actions.RIGHT:#action not in [Actions.LEFT,Actions.HALT]:
				reward+=40

		#if turbo_stuck and not self.safe_exit:
		#	reward+=-20
		# if not cheese_eaten:	
		# 	if self.cheese_top and action not in [Actions.DOWN,Actions.HALT]:
		# 		reward+=10
		# 	if not self.cheese_top and action not in [Actions.UP,Actions.HALT]:
		# 		reward+=10
		# 	if self.cheese_left and action not in [Actions.RIGHT,Actions.HALT]:
		# 		reward+=10
		# 	if not self.cheese_left and action not in [Actions.LEFT,Actions.HALT]:
		# 		reward+=10


		#if not self.can_move(action,pacman): #and action!= Actions.HALT:
		#	reward+=-5
		



		#if log:
		#	print(log+"\n-----")
		#danger_red_y,danger_red_x,ghost_facing=self.check_ghost_is_coming(self.entities[1]) #danger preciso
		#danger_pink_y,danger_pink_x,ghost_facing=self.check_ghost_is_coming(self.entities[2]) #danger preciso
		#for danger in [danger_red_y,danger_red_x,danger_pink_y,danger_pink_x]:
		#	if danger:
		#		reward+=-40
			
		#print(action)
		#	print("can't move: "+ Actions(action).name)
		#else:
		#	reward=-5
		#se sono in pericolo (non è preciso perché ignora i muri) allora non ti premio
		#red=self.entities[ENTITIES.RED.value]
		#for entity in self.entities:
		#	if entity.name=="pacman":
		#		continue
			#is_goodboy=self.check_pacman_is_goodboy(ghost_facing)
			#danger_reward=-100
			#danger_reward=0
			#warning_reward=0
			#warning_reward=-15
			# if pacman.invincibility_timestamp> self.graphics.frame_iteration -425:
			# 	#danger_reward=0
			# 	#warning_reward=0
			# 	#pacman.invincible=1
			# else:
			# 	pacman.invincible=0
			# 	pacman.set_normal_sprite()
			#danger_y,danger_x,ghost_facing=self.check_ghost_is_coming(entity) #danger preciso
			#if danger_y:
			#	reward+=-20
			#	print("DANGER PRECISO")
			#if danger_x:
			#	reward+=danger_reward
			#	print("DANGER PRECISO")
		#if self.stuck and not self.safe_exit:
		#if self.stuck: #TODO se cosi' dovrei sovrascrivere il -reward danger
		#	reward+=-15
		#print(self.entities[1].distance_from_pacman)
		#if not self.safe_exit:

			

		self.check_game_over()
		if self.is_game_over:
				reward=-4000
				self.n_games+=1
		if self.check_game_won():
			#reward=100
			self.n_games+=1
			#self.score+=1000
			self.is_game_over=1
		self.graphics.draw_window(self.debug,str(reward))
		#print(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
		#print(old_red_dist, self.red_dist)
		#print(reward)
		#print(self.red_getting_closer)
		#if self.safe_exit:
		#	print(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
		return reward, self.is_game_over, self.score	
	
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
		#if red.pos_in_grid_y<=pacman.pos_in_grid_y<=pink.pos_in_grid_y or pink.pos_in_grid_y<=pacman.pos_in_grid_y<=red.pos_in_grid_y:
		#	if red.pos_in_grid_y != pink.pos_in_grid_y:
		#		return 1
		#if red.pos_in_grid_x<=pacman.pos_in_grid_x<=pink.pos_in_grid_x or pink.pos_in_grid_x<=pacman.pos_in_grid_x<=red.pos_in_grid_x:
		#	if red.pos_in_grid_x != pink.pos_in_grid_x:
		#		return 1
		#return 0
	
 
	def check_game_over(self):
		pacman=self.entities[ENTITIES.PACMAN.value]
		red=self.entities[ENTITIES.RED.value]
		pink=self.entities[ENTITIES.PINK.value]
		self.is_game_over= (pacman.pos_in_grid_y == red.pos_in_grid_y and pacman.pos_in_grid_x == red.pos_in_grid_x) or (pacman.pos_in_grid_y == pink.pos_in_grid_y and pacman.pos_in_grid_x == pink.pos_in_grid_x)
		poss=0
		for i in range(4):
			poss+=self.possibilities[i]
		self.is_game_over= self.is_game_over or (self.am_i_in_sandwitch() and poss==0)
		#if self.is_game_over:
			#print(self.game_over)
		#if entity.pos_in_grid_x== pacman.pos_in_grid_x and entity.pos_in_grid_y == pacman.pos_in_grid_y:
		#e_rect=pygame.Rect(entity.rect.x,entity.rect.y,*entity.IMAGE.get_size())
		#p_rect=pygame.Rect(pacman.rect.x,pacman.rect.y,*pacman.IMAGE.get_size())
		#if p_rect.colliderect(e_rect):
		#	self.game_over=True
		#	entity.reset_position()
		#	self.game_over=1
		#	return True

			#if entity.pos_in_grid_y== pacman.pos_in_grid_y and entity.pos_in_grid_x==pacman.pos_in_grid_x:
			#		return True
		#return False
				#if pacman.rect.colliderect(entity.rect):
					#self.game_over=True
				#	return True
		#if self.grid[pacman.pos_in_grid_y][pacman.pos_in_grid_x]>1:
		#	print("WTF")
		#	return True
		#self.game_over=False
		#return False
	#def can_move_neighbours_cells(self,entity):
	#	 return self.can_move(Actions.LEFT,entity),self.can_move(Actions.RIGHT,entity),self.can_move(Actions.UP,entity),self.can_move(Actions.DOWN,entity)
	
	def right_cheese_zone(self,cheese_y,cheese_x):
		...
		#return self.get_zone(self.entities[0].y,self.entities[0].x)==self(cheese_y,cheese_x)
	def get_zone(self,y,x) -> tuple[int, int]:
		return y>14,x>14
		#zone=0
		#if y>14:
		#	zone+=1
		#if x>14:
		#	zone+=2
		#return zone
		
	def cheese_per_action(self,action,entity):
		x=entity.pos_in_grid_x
		y=entity.pos_in_grid_y
		n=0
		for k in range(1):
			y=y+k
			y = min(y, 30)
			#print(y)
			cell=self.grid[y][x]
			#print(y,cell)
			#print(cell)
			if action==Actions.LEFT:
				while x>-1 and cell!=2:
					x-=1
					cell=self.grid[y][x]
					if cell == 1:
						n += 1
			if action==Actions.RIGHT:
				while x<27 and cell!=2:
					x+=1
					cell=self.grid[y][x]
					if cell == 1:
						n += 1
			if action==Actions.UP:
				while y>-1 and cell!=2:
					y-=1
					cell=self.grid[y][x]
					if cell == 1:
						n += 1
			if action==Actions.DOWN:
				while y<30 and cell!=2:
					y+=1
					cell=self.grid[y][x]
					if cell == 1:
						n += 1
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
		#game.graphics.draw_window(game.debug,"")
		action=check_keyboard() #questo ora e manuale, poi ci pensera' l'agents
		#game.get_closest_cheese()
		game.get_closest_safe_exit()
		if game.is_game_over:#and not pacman.invincible:
			game.reset()
		game.play_step(action) #ignorare il parametro per ora
		game.play_ghost()
		#game.get_closest_cheese()
		#print(game.BEST)
		#print(game.score)
		#pacman=game.entities[ENTITIES.PACMAN.value]
		#game.check_game_over() 
		#print(game.is_game_over)
		if game.is_game_over:#and not pacman.invincible:
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
			
			#pacman=game.entities[0]
			#game.get_closest_cheese2(pacman.pos_in_grid_y,pacman.pos_in_grid_x)
			#game.get_closest_cheese()

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
