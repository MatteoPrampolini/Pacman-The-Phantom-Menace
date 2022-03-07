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
ENTITY_WIDTH, ENTITY_HEIGHT = 32, 32
#colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
GREEN =(50, 168, 86)
GOLD= (255,215,0)
COIN= (224, 209, 209)
YELLOW = (255,241,0)

class PacGraphic:
		
	def __init__(self,WIDTH,HEIGHT):
		self.w = WIDTH
		self.h = HEIGHT
		self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
		self.MAP = pygame.image.load(os.path.join('Assets', 'map.png'))
		self.entities = None
		self.grid = None
		self.font = pygame.font.Font(os.path.join('Assets', 'emulogic.ttf'),25)
		self.timer = 0
		self.clock = pygame.time.Clock()
		self.FPS = 40
		self.frame_iteration = 0

		
	def reset(self):
		self.timer= 0
		self.frame_iteration = 0
		self.old_iter=0
		for entity in self.entities:
			#entity.pos_in_grid_y=entity.default_y
			#entity.pos_in_grid_x=entity.default_x
			entity.reset_position()
			entity.set_pos_in_grid()
			if entity.name=="pacman":
				entity.reset_invincibility()

	def get_grid(self,grid):
		self.grid=grid
	
	def get_entities(self,entities):
		self.entities=entities
	
	def update_time(self,time):
		self.timer=time
	
	def highlight_specific_cell(self,y,x):
		tmp = pygame.Rect(0,0, CELL_DIM, CELL_DIM)
		tmp.y=OFFSET_Y+y*CELL_DIM			
		tmp.x=OFFSET_X+x*CELL_DIM
		pygame.draw.rect(self.WIN,RED,tmp)
		pygame.display.update()

	def draw_grid(self): #per il debug, non viene chiamata nella versione finale
		tmp = pygame.Rect(0,0, CELL_DIM, CELL_DIM)
		COLORS=[WHITE,GOLD,BLUE,BLACK]
		for row in range(GRID_ROWS):
			for column in range(GRID_COLS):
				tmp.y=OFFSET_Y+row*CELL_DIM			
				tmp.x=OFFSET_X+column*CELL_DIM
				pygame.draw.rect(self.WIN,COLORS[self.grid[row][column]],tmp)
	
	def window_to_grid(self,x,y):
		#x=(x-OFFSET_X+width//2)//CELL_DIM
		#y=(y-OFFSET_Y+height//2)//CELL_DIM
		x=(x)//CELL_DIM
		y=(y)//CELL_DIM
		return x,y

	def grid_to_window(self,row,col): 
		
		x=col*CELL_DIM
		y=row*CELL_DIM
		return x,y
	
	def draw_entities(self):
		for entity in self.entities:
			if entity.name == "pacman" :
				#immagine,posizione, punto iniziale frame da prendere = (numero,0), quanto è grande la singola sprite = (33,33)
				self.WIN.blit(entity.IMAGE, (entity.rect.x - 8, entity.rect.y - 8), (((entity.sprite_frame * 33) + (entity.facing.value * (33*4))), 0, 33, 33))
				if self.frame_iteration >= entity.next_frame:
					entity.sprite_frame = ((entity.sprite_frame + 1) % 4)
					print(entity.sprite_frame , entity.facing.value)
					entity.next_frame += 8
			else:
				self.WIN.blit(entity.IMAGE, (entity.rect.x - 8, entity.rect.y - 8), (((entity.sprite_frame * 32) + (entity.facing.value * (32*2))), 0, 32, 32))
				if self.frame_iteration >= entity.next_frame:
					entity.sprite_frame = ((entity.sprite_frame + 1) % 2)
					entity.next_frame += 40
				#if scared usa altre sprite

			pass

	def draw_window(self,debug):
		self.WIN.fill((0, 0, 0))
		self.WIN.blit(self.MAP, (0, 0))
		
		if debug:
			self.draw_grid()
			for entity in self.entities:
				pygame.draw.rect(self.WIN,GREEN,entity.rect)
		
		self.draw_coins()
		self.draw_entities()
		
		self.draw_text()
		self.clock.tick(self.FPS)
		self.frame_iteration+=1
		pygame.display.update()
	
	
	def draw_coins(self):
		tmp = pygame.Rect(0,0, CELL_DIM//2, CELL_DIM//2)
		for row in range(GRID_ROWS):
			for column in range(GRID_COLS):
				tmp.y=OFFSET_Y+row*CELL_DIM			
				tmp.x=OFFSET_X+column*CELL_DIM
				if self.grid[row][column]==1:
					pygame.draw.circle(self.WIN,COIN,(tmp.x+8,tmp.y+8),CELL_DIM//4)
				if self.grid[row][column]==-1:
					pygame.draw.circle(self.WIN,COIN,(tmp.x+8,tmp.y+8),CELL_DIM//2)
	
	
	def draw_text(self):
		if self.timer < 2.5:
			ready_lbl = self.font.render("READY!", True, YELLOW)
			x,y=self.grid_to_window(row=19,col=10)
			self.WIN.blit(ready_lbl,[x-6,y+6])