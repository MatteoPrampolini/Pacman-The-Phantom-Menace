import pygame
import os
import sys
import numpy as np
from enum import Enum
from graphics import CELL_DIM,OFFSET_X,OFFSET_Y #,FPS
import pathfinding
class FACING(Enum):
	NORTH = 0
	SOUTH= 1
	WEST = 2
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
		self.facing= FACING.WEST
		self.old_action=Actions.UP
		#self.pos_in_grid_x=0
		#self.pos_in_grid_y=0
		self.VEL = 1#2*FPS/60
	

	def reset_position(self):
		self.set_rect(self.default_x,self.default_y,self.rect.w,self.rect.h)
	
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
		
		#self.VEL = int(2*FPS/60)
		self.reset_invincibility()
		#self.VEL=2
	
	def set_invincibility_sprite(self):
		self.IMAGE=pygame.image.load(os.path.join('Assets', 'pac-super.png'))
	def set_normal_sprite(self):
		self.IMAGE=pygame.image.load(os.path.join('Assets', 'pac-tmp.png'))

	def reset_invincibility(self):
			self.invincible=0
			self.invincibility_timestamp=-9999
			self.set_normal_sprite()
class Ghost(Entity):
	def __init__(self,img_path,grid :np.ndarray,name="no name"):
		super().__init__(img_path,name)
		self.solver= pathfinding.solver(grid)
		#self.VEL = int(1*FPS/60)
		self.VEL=1
		self.last_action=Actions.HALT
		self.distance_from_pacman=12
		self.old_pos=[self.default_y,self.default_x]
		self.path=[]
		
		self.old_path=None
	def get_new_path(self,pacman):
		pass

	def reset_position(self):
		self.set_rect(self.default_x,self.default_y,self.rect.w,self.rect.h)
		self.old_distance=12
		self.old_pos=[self.default_y,self.default_x]
	
	
class RedGhost(Ghost):
	def __init__(self,img_path,grid,name="no name"):
		super().__init__(img_path,grid,name)
		
	def get_new_path(self,pacman):
		px=pacman.pos_in_grid_x
		py=pacman.pos_in_grid_y
		pacman_facing=pacman.facing
		x=self.pos_in_grid_x
		y=self.pos_in_grid_y
		self.old_distance=self.distance_from_pacman
		self.old_pos=[y,x]
		self.path,self.distance_from_pacman = self.solver.get_path(py,px,y,x)
		#if len(self.path)<=1:
		return self.path[0]
		#return self.path

class PinkGhost(Ghost):
	def __init__(self,img_path,grid,name="no name"):
		super().__init__(img_path,grid,name)
	
	def get_new_path(self,pacman):
		px=pacman.pos_in_grid_x
		py=pacman.pos_in_grid_y
		pacman_facing=pacman.facing
		tmpx=px
		tmpy=py
		i=8
		grid=self.solver.a
		if pacman_facing==FACING.NORTH:
			while i>0:
				py=tmpy-i
				if py<0:
					py=0
				if grid[py][px]<2:
					break
				i-=1
		if pacman_facing== FACING.SOUTH:
			while i>0:
				py=tmpy+i
				if py>30:
					py=30
				if grid[py][px]<2:
					break
				i-=1
		if pacman_facing== FACING.WEST:
			while i>0:
				px=tmpx-i
				if px<0:
					px=0
				if grid[py][px]<2:
					break
				i-=1
		#print(i)
		if pacman_facing== FACING.EAST:
			while i>0:
				px=tmpx+i
				if px>27:
					px=27
				if grid[py][px]<2:
					break
				i-=1
		x=self.pos_in_grid_x
		y=self.pos_in_grid_y
		self.old_pos=[y,x]
		self.path,self.distance_from_pacman = self.solver.get_path(py,px,y,x)
		return self.path[0]