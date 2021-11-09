import pygame
import os
import sys
import numpy as np
import graphics as gp
class Actions():
	UP =  [1,0,0,0]
	DOWN = [0,1,0,0]
	LEFT = [0,0,1,0]
	RIGHT = [0,0,0,1]

pygame.font.init()	# text init
pygame.mixer.init()	 # sound init

WIDTH, HEIGHT = 448, 576
pygame.display.set_caption("Pacman")

#game settings
FPS = 60
VEL = 3

class Game():
	def __init__(self, w=WIDTH, h=HEIGHT):
		self.w=w
		self.h=h
		self.clock = pygame.time.Clock()
		self.graphics = gp.PacGraphic(w,h) #questa classe gestisce tutto cio' che e' grafico.
		#nella classe game lavoriamo solo con le coordinate della grid, dei pixel non ci interessa.
		self.reset()
		
	def reset(self):
		self.grid=np.array([[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2], [2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2], [2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2], [2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2], [2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2], [2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2], [2,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,2], [2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2], [2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2], [2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2], [2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2], [3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3], [3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3], [3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3], [2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2], [0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0], [2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2], [3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3], [3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3], [3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3], [2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2], [2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2], [2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2], [2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2], [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2], [2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2], [2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2], [2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2], [2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2], [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]])
		self.grid=self.grid[::-1] #devo flipparlo perché non ho lo sbatti di invertire l'ordine delle righe
		self.graphics.reset()
		self.graphics.set_grid(self.grid)
		self.debug=False
		self.is_running=True
		self.is_game_over=False
	def handle_red_movement(self,keys_pressed):
		red= self.graphics.red
		if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0:  # LEFT
			if self.can_move(Actions.LEFT,red):
				red.x -= VEL
		if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:	# RIGHT
			if self.can_move(Actions.RIGHT,red):
				red.x += VEL
		if keys_pressed[pygame.K_UP] and red.y - VEL > 0:	# UP
			if self.can_move(Actions.UP,red):
				red.y -= VEL
		if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:	 # DOWN
			if self.can_move(Actions.DOWN,red):
				red.y += VEL
	def handle_pac_movement(self,keys_pressed):
		pac= self.graphics.pac
		if keys_pressed[pygame.K_a] and pac.x - VEL > 0:  # LEFT
			if self.can_move(Actions.LEFT,pac):
				pac.x -= VEL
		if keys_pressed[pygame.K_d] and pac.x + VEL + pac.width < WIDTH:	# RIGHT
			if self.can_move(Actions.RIGHT,pac):
				pac.x += VEL
		if keys_pressed[pygame.K_w] and pac.y - VEL > 0:	# UP
			if self.can_move(Actions.UP,pac):
				pac.y -= VEL
		if keys_pressed[pygame.K_s] and pac.y + VEL + pac.height < HEIGHT:	 # DOWN
			if self.can_move(Actions.DOWN,pac):
				pac.y += VEL
		x,y=self.graphics.coords_to_matrix(pac)
		if self.grid[y][x]==1:
			self.grid[y][x]=0

	def can_move(self,action,rect):
		x,y=self.graphics.coords_to_matrix(rect)
		if action == Actions.UP and self.grid[y-1,x]==2:
			return False
		if action == Actions.DOWN and self.grid[y+1,x]==2:
			return False
		if action == Actions.LEFT and self.grid[y,x-1]==2:
			return False
		if action == Actions.RIGHT and self.grid[y,x+1]==2:
			return False
		return True
		
		
		
def main():

	game= Game()
	while True:
		check_for_events(game)
		if not game.is_running:
			continue
		keys_pressed = pygame.key.get_pressed()

		game.clock.tick(FPS)
		game.handle_red_movement(keys_pressed)
		game.handle_pac_movement(keys_pressed)
		game.graphics.draw_window(game.debug)

		if game.is_game_over:
			game.reset()
def check_for_events(game):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYUP: #keyup è meglio di keydown se vuoi premere il tasto una volta sola
				if event.key == pygame.K_p: #if P is pressed, toggle pause
					game.is_running=not game.is_running
				if event.key == pygame.K_m: #if P is pressed, toggle pause
					game.debug=not game.debug
if __name__ == "__main__":
	main()
