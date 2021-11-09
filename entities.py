import pygame
import os
import sys
import numpy as np
from graphics import CELL_DIM,OFFSET_X,OFFSET_Y
class Entity:
	def __init__(self,img_path,x=0,y=0,name="no name"):
		self.name=name
		self.IMAGE = pygame.image.load(img_path)
		self.rect = pygame.Rect(0,0,0,0)
		self.set_rect(x,y,*self.IMAGE.get_size())
		self.default_pos=[x,y]
		
	def reset_position(self):
		self.rect.x,self.rect.y= self.default_pos
	
	def set_rect(self,x,y,w,h):
		self.rect.x=x
		self.rect.x=y
		self.rect.width=w
		self.rect.height=h
	
	def coords_to_matrix(self):
		x=(self.rect.x-OFFSET_X+self.rect.width//2)//CELL_DIM
		y=(self.rect.y-OFFSET_Y+self.rect.height//2)//CELL_DIM
		return x,y
		
class Pacman(Entity):
	def __init__(self,img_path,x=0,y=0,name="no name"):
		super().__init__(img_path,x,y,name)
	
class Ghost(Entity):
	def __init__(self,img_path,x=0,y=0,name="no name"):
		super().__init__(img_path,x,y,name)
		
class RedGhost(Ghost):
	def __init__(self,img_path,x=0,y=0,name="no name"):
		super().__init__(img_path,x,y,name)