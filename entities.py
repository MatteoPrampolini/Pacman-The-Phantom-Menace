import pygame
import os
import sys
import numpy as np
from graphics import CELL_DIM,OFFSET_X,OFFSET_Y
class Entity:
	def __init__(self,img_path,name="no name"):
		self.name=name
		self.IMAGE = pygame.image.load(img_path)
		self.rect = pygame.Rect(0,0,0,0)
		#self.set_rect(x,y,*self.IMAGE.get_size())
		self.default_x=0
		self.default_y=0
		
	def reset_position(self):
		self.rect.x= self.default_x
		self.rect.y= self.default_y
	
	def set_rect(self,x,y,w,h):
		self.rect.x=x
		self.rect.y=y
		self.rect.width=w
		self.rect.height=h
	
	def window_to_grid(self):
		x=(self.rect.x-OFFSET_X+self.rect.width//2)//CELL_DIM
		y=(self.rect.y-OFFSET_Y+self.rect.height//2)//CELL_DIM
		return x,y
		
class Pacman(Entity):
	def __init__(self,img_path,name="no name"):
		super().__init__(img_path,name)

class Ghost(Entity):
	def __init__(self,img_path,name="no name"):
		super().__init__(img_path,name)
	
class RedGhost(Ghost):
	def __init__(self,img_path,name="no name"):
		super().__init__(img_path,name)