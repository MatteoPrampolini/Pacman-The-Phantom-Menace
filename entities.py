import pygame
import os
import sys
import numpy as np
from enum import Enum
from graphics import CELL_DIM,OFFSET_X,OFFSET_Y
import pathfinding
class FACING(Enum):
	NORTH = 0,
	SOUTH= 1,
	WEST = 2,
	EAST= 3
class Actions():
	UP 	 = [1,0,0,0,0]
	DOWN = [0,1,0,0,0]
	LEFT = [0,0,1,0,0]
	RIGHT= [0,0,0,1,0]
	HALT = [0,0,0,0,1]
class Entity:
	def __init__(self,img_path,name="no name"):
		self.name=name
		self.IMAGE = pygame.image.load(img_path)
		self.rect = pygame.Rect(0,0,0,0)
		#self.set_rect(x,y,*self.IMAGE.get_size())
		self.default_x=0
		self.default_y=0
		self.facing= FACING.EAST
		self.pos_in_grid_x=0
		self.pos_in_grid_y=0
		self.VEL = 3
	def reset_position(self):
		self.rect.x= self.default_x
		self.rect.y= self.default_y
	
	def set_pos_in_grid(self):
		self.pos_in_grid_x,self.pos_in_grid_y=self.window_to_grid()

	def set_rect(self,x,y,w,h):
		self.rect.x=x
		self.rect.y=y
		self.rect.width=w
		self.rect.height=h
	

		
	def window_to_grid(self):
		x=(self.rect.x-OFFSET_X+self.rect.width//2)//CELL_DIM
		y=(self.rect.y-OFFSET_Y+self.rect.height//2)//CELL_DIM
		
		
		return x,y
	def __str__(self):
		x=self.rect.x-OFFSET_X+self.rect.width//2
		y=self.rect.y-OFFSET_Y+self.rect.height//2
		return self.name.upper()+"\t"+str(self.pos_in_grid_y)+","+str(self.pos_in_grid_x)+"\t"+str(x)+","+str(y)
		
	
class Pacman(Entity):
	def __init__(self,img_path,name="no name"):
		super().__init__(img_path,name)
		self.VEL = 3
class Ghost(Entity):
	def __init__(self,img_path,grid :np.ndarray,name="no name"):
		super().__init__(img_path,name)
		self.solver= pathfinding.solver(grid)
		self.VEL = 2
		self.last_action=Actions.HALT
		self.old_path=None
	def get_new_path(self,dx,dy):
		x=self.pos_in_grid_x
		y=self.pos_in_grid_y
		p = self.solver.get_path(dy,dx,y,x)
		if not p:
			return (-1,-1)
		if p:
			return p
	
class RedGhost(Ghost):
	def __init__(self,img_path,grid,name="no name"):
		super().__init__(img_path,grid,name)

class PinkGhost(Ghost):
	def __init__(self,img_path,grid,name="no name"):
		super().__init__(img_path,grid,name)