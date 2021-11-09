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

class PacGraphic:
	
	def __init__(self,WIDTH,HEIGHT):
		self.w=WIDTH
		self.h=HEIGHT
		self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
		self.MAP = pygame.image.load(os.path.join('Assets', 'map.png'))
		self.RED_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'red-tmp.png')), (ENTITY_WIDTH, ENTITY_HEIGHT))
		self.PAC_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'pac-tmp.png')), (ENTITY_WIDTH, ENTITY_HEIGHT))
		self.red = pygame.Rect(WIDTH//2, HEIGHT//2, ENTITY_WIDTH, ENTITY_HEIGHT)
		self.pac = pygame.Rect(WIDTH//2, HEIGHT//2, ENTITY_WIDTH, ENTITY_HEIGHT)
		self.grid = None
	def reset(self):
		self.pac.x=int(self.w/2)-int(self.pac.width/2)
		self.pac.y=int(self.h/2)-70
		self.red.x=int(self.w/2)-int(self.red.width/2)
		self.red.y=int(self.h/2)-25
	
	def set_grid(self,grid):
		self.grid=grid
		
	def draw_grid(self): #per il debug, non viene chiamata nella versione finale
		tmp = pygame.Rect(0,0, CELL_DIM, CELL_DIM)
		COLORS=[WHITE,YELLOW,BLUE,BLACK]
		for row in range(GRID_ROWS):
			for column in range(GRID_COLS):
				tmp.y=OFFSET_Y+row*CELL_DIM			
				tmp.x=OFFSET_X+column*CELL_DIM
				pygame.draw.rect(self.WIN,COLORS[self.grid[row][column]],tmp)
	
	def draw_window(self,debug):

		self.WIN.fill((0, 0, 0))
		self.WIN.blit(self.MAP, (0, 0))
		if debug:
			self.draw_grid(self.grid)
		self.WIN.blit(self.RED_IMAGE, (self.red.x, self.red.y))
		self.WIN.blit(self.PAC_IMAGE, (self.pac.x, self.pac.y))
		self.draw_coins()
		pygame.display.update()
	
	def draw_coins(self):
		tmp = pygame.Rect(0,0, CELL_DIM//2, CELL_DIM//2)
		for row in range(GRID_ROWS):
			for column in range(GRID_COLS):
				tmp.y=OFFSET_Y+row*CELL_DIM			
				tmp.x=OFFSET_X+column*CELL_DIM
				if self.grid[row][column]==1:
					pygame.draw.circle(self.WIN,COIN,(tmp.x+8,tmp.y+8),CELL_DIM//4)
	
	def coords_to_matrix(self,rect):
		y=(rect[1]-OFFSET_Y+rect[3]//2)//CELL_DIM
		x=(rect[0]-OFFSET_X+rect[2]//2)//CELL_DIM
		return x,y
	
