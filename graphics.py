import pygame
import os
import sys
import numpy as np
#drawing settings
OFFSET_X=0
OFFSET_Y=48
GRID_ROWS=31 
GRID_COLS=28
CELL_DIM=16
ENTITY_WIDTH, ENTITY_HEIGHT = 25, 25
#colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
GREEN =(50, 168, 86)
YELLOW= (255,215,0)
COIN= (224, 209, 209)
#ENTITY_OFFSET_X=5
from main import ENTITIES
class PacGraphic:
	
	def __init__(self,WIDTH,HEIGHT):
		self.w=WIDTH
		self.h=HEIGHT
		self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
		self.MAP = pygame.image.load(os.path.join('Assets', 'map.png'))
		self.entities=None
		self.grid = None
	def reset(self):
		for entity in self.entities:
			entity.reset_position()
	def get_grid(self,grid):
		self.grid=grid
	
	def get_entities(self,entities):
		self.entities=entities
		
	def draw_grid(self): #per il debug, non viene chiamata nella versione finale
		tmp = pygame.Rect(0,0, CELL_DIM, CELL_DIM)
		COLORS=[WHITE,YELLOW,BLUE,BLACK]
		for row in range(GRID_ROWS):
			for column in range(GRID_COLS):
				tmp.y=OFFSET_Y+row*CELL_DIM			
				tmp.x=OFFSET_X+column*CELL_DIM
				pygame.draw.rect(self.WIN,COLORS[self.grid[row][column]],tmp)
	
	def grid_to_window(self,row,col): 
		
		x=col*CELL_DIM+OFFSET_X
		y=row*CELL_DIM+OFFSET_Y
		return x,y
	
	def draw_entities(self):
		for entity in self.entities:
			self.WIN.blit(entity.IMAGE, (entity.rect.x,entity.rect.y))
	def draw_window(self,debug):

		self.WIN.fill((0, 0, 0))
		self.WIN.blit(self.MAP, (0, 0))
		if debug:
			self.draw_grid()
			for entity in self.entities:
				pygame.draw.rect(self.WIN,GREEN,entity.rect)
		
		self.draw_coins()
		self.draw_entities()
		pygame.display.update()
	
	
	def draw_coins(self):
		tmp = pygame.Rect(0,0, CELL_DIM//2, CELL_DIM//2)
		for row in range(GRID_ROWS):
			for column in range(GRID_COLS):
				tmp.y=OFFSET_Y+row*CELL_DIM			
				tmp.x=OFFSET_X+column*CELL_DIM
				if self.grid[row][column]==1:
					pygame.draw.circle(self.WIN,COIN,(tmp.x+8,tmp.y+8),CELL_DIM//4)
	
