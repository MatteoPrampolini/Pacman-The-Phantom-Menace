import arcade, os, sys
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.ui_style import UIStyle
import startGame
import menuView
window3= None
gridRows=31 
gridCols=28
debug=0
movspeed = 5

#nel gioco di default prime 3 e ultime 2 rows sono vuote.


class GameView(arcade.View):
	def __init__(self, window):
		"""
		Initializer
		"""

		super().__init__()
		# buttons, text e simili
		self.ui_manager = UIManager()
		# le sprite
		self.sprites = arcade.SpriteList()
		# lista che contiene i player
		self.player_list = None
		# proprietà P1
		self.player1 = None
		# proprietà P2
		self.player2 = None
		# proprietà pacman
		self.pacman = None

		# Track the current state of what key is pressed
		#P1
		self.left_pressed = False
		self.right_pressed = False
		self.up_pressed = False
		self.down_pressed = False
		#P2
		self.a_pressed = False
		self.d_pressed = False
		self.w_pressed = False
		self.s_pressed = False


		# inizializzazione griglia
		self.grid = []
		for row in range(gridRows):
			self.grid.append([])
			for column in range(gridCols):
				self.grid[row].append(1)
		# print(self.grid)
		# print(self.grid[0][0])
		self.resetGrid()
		self.fps = -1
		global window3
		window3 = self.window
		# sprites
		self.setup()

	def setup(self):

		self.ui_manager.purge_ui_elements()
		width,height= self.window.get_size()
		menuBtn = MenuBTN(
			'Menu',
			center_x= width-100,
			center_y= height-30,
			width=150,
			height=30
		)
		self.ui_manager.add_ui_element(menuBtn)

		debugBtn = DebugBTN(
			'Debug',
			center_x= width-100,
			center_y= height/2+50,
			width=100,
			height=30
		)
		self.ui_manager.add_ui_element(debugBtn)

		self.sprites.append(arcade.Sprite(startGame.PATH+'/assets/map.png', scale=1.0, center_x=width/2, center_y=height/2))

		#tek
		# TODO: devo capire come trovare la posizione precisa in cui mettere il fantasmino
		# TODO: fare la roba per il movimento (dove può andare)
		# TODO: aggiustare la dimensione delle sprite e la movspeed del player
		self.player_list = arcade.SpriteList()
		self.player1 = arcade.AnimatedWalkingSprite()
		self.player2 = arcade.AnimatedWalkingSprite()
		self.pacman = arcade.AnimatedWalkingSprite()

		# setup texture player 1
		self.player1.stand_right_textures = []
		self.player1.walk_right_textures = []
		for i in range(2):
			self.player1.stand_right_textures.append(
				arcade.load_texture("assets/sprites.png", x=0, y=i * 49, width=49, height=49))
			self.player1.walk_right_textures.append(
				arcade.load_texture("assets/sprites.png", x=0, y=i * 49, width=49, height=49))

		self.player1.stand_left_textures = []
		self.player1.walk_left_textures = []
		for i in range(2):
			self.player1.stand_left_textures.append(
				arcade.load_texture("assets/sprites.png", x=0, y=202 + (i * 49), width=49, height=49))
			self.player1.walk_left_textures.append(
				arcade.load_texture("assets/sprites.png", x=0, y=202 + (i * 49), width=49, height=49))

		self.player1.walk_up_textures = []
		for i in range(2):
			self.player1.walk_up_textures.append(
				arcade.load_texture("assets/sprites.png", x=0, y=300 + (i * 49), width=49, height=49))

		self.player1.walk_down_textures = []
		for i in range(2):
			self.player1.walk_down_textures.append(
				arcade.load_texture("assets/sprites.png", x=0, y=101 + (i * 49), width=49, height=49))

		# setup texture player 2
		self.player2.stand_right_textures = []
		self.player2.walk_right_textures = []
		for i in range(2):
			self.player2.stand_right_textures.append(
				arcade.load_texture("assets/sprites.png", x=99, y=i * 49, width=49, height=49))
			self.player2.walk_right_textures.append(
				arcade.load_texture("assets/sprites.png", x=99, y=i * 49, width=49, height=49))

		self.player2.stand_left_textures = []
		self.player2.walk_left_textures = []
		for i in range(2):
			self.player2.stand_left_textures.append(
				arcade.load_texture("assets/sprites.png", x=99, y=202 + (i * 49), width=49, height=49))
			self.player2.walk_left_textures.append(
				arcade.load_texture("assets/sprites.png", x=99, y=202 + (i * 49), width=49, height=49))

		self.player2.walk_up_textures = []
		for i in range(2):
			self.player2.walk_up_textures.append(
				arcade.load_texture("assets/sprites.png", x=99, y=300 + (i * 49), width=49, height=49))

		self.player2.walk_down_textures = []
		for i in range(2):
			self.player2.walk_down_textures.append(
				arcade.load_texture("assets/sprites.png", x=99, y=101 + (i * 49), width=49, height=49))

		# setup texture pacman
		self.pacman.stand_right_textures = []
		self.pacman.walk_right_textures = []
		for i in range(3):
			self.pacman.stand_right_textures.append(
				arcade.load_texture("assets/sprites.png", x=850, y=i * 49, width=49, height=49))
			self.pacman.walk_right_textures.append(
				arcade.load_texture("assets/sprites.png", x=850, y=i * 49, width=49, height=49))

		self.pacman.stand_left_textures = []
		self.pacman.walk_left_textures = []
		for i in range(3):
			self.pacman.stand_left_textures.append(
				arcade.load_texture("assets/sprites.png", x=850, y=302 + (i * 49), width=49, height=49))
			self.pacman.walk_left_textures.append(
				arcade.load_texture("assets/sprites.png", x=850, y=302 + (i * 49), width=49, height=49))

		self.pacman.walk_up_textures = []
		for i in range(3):
			self.pacman.walk_up_textures.append(
				arcade.load_texture("assets/sprites.png", x=850, y=450 + (i * 49), width=49, height=49))

		self.pacman.walk_down_textures = []
		for i in range(3):
			self.pacman.walk_down_textures.append(
				arcade.load_texture("assets/sprites.png", x=850, y=150 + (i * 49), width=49, height=49))

		self.player1.center_x = width/2
		self.player1.center_y = height/2

		self.player2.center_x = width / 2
		self.player2.center_y = height / 2

		self.pacman.center_x = width / 2
		self.pacman.center_y = height / 2

		self.player_list.append(self.player1)
		self.player_list.append(self.player2)
		self.player_list.append(self.pacman)


	def on_hide_view(self):
		self.ui_manager.unregister_handlers()

	def on_draw(self):
		arcade.start_render()
		self.sprites.draw()
		if debug:
			self.drawGrid()
		width, height = self.window.get_size()

		arcade.draw_text("fps: " + str(self.fps), 10, height - 30, arcade.color.WHITE, 15)
		arcade.draw_text("SESSOLONE", 100, height - 30, arcade.color.WHITE, 15)

		self.player_list.draw()

	def on_update(self, delta_time):
		self.fps = round(1/delta_time)

		# gestione movimento P1
		# Calculate speed based on the keys pressed
		self.player1.change_x = 0
		self.player1.change_y = 0
		if self.up_pressed and not self.down_pressed:
			self.player1.change_y = movspeed
		elif self.down_pressed and not self.up_pressed:
			self.player1.change_y = -movspeed
		if self.left_pressed and not self.right_pressed:
			self.player1.change_x = -movspeed
		elif self.right_pressed and not self.left_pressed:
			self.player1.change_x = movspeed

		self.player2.change_x = 0
		self.player2.change_y = 0
		if self.w_pressed and not self.s_pressed:
			self.player2.change_y = movspeed
		elif self.s_pressed and not self.w_pressed:
			self.player2.change_y = -movspeed
		if self.a_pressed and not self.d_pressed:
			self.player2.change_x = -movspeed
		elif self.d_pressed and not self.a_pressed:
			self.player2.change_x = movspeed

		# Call update to move the sprite
		self.player_list.update()
		self.player_list.update_animation()

	def on_key_press(self, key, modifiers):
		"""Called whenever a key is pressed. """

		# movimento player 1 semplice
		#if key == arcade.key.UP:
		#	self.player1.change_y = movspeed
		#if key == arcade.key.DOWN:
		#	self.player1.change_y = -movspeed
		#if key == arcade.key.LEFT:
		#	self.player1.change_x = -movspeed
		#if key == arcade.key.RIGHT:
		#	self.player1.change_x = movspeed

		# movimento player 1 migliore
		if key == arcade.key.UP:
			self.up_pressed = True
		elif key == arcade.key.DOWN:
			self.down_pressed = True
		elif key == arcade.key.LEFT:
			self.left_pressed = True
		elif key == arcade.key.RIGHT:
			self.right_pressed = True
		# movimento player 2
		if key == arcade.key.W:
			self.w_pressed = True
		elif key == arcade.key.S:
			self.s_pressed = True
		elif key == arcade.key.A:
			self.a_pressed = True
		elif key == arcade.key.D:
			self.d_pressed = True

	def on_key_release(self, key, key_modifiers):
		"""Called when the user releases a key. """
		# print(key, key_modifiers)

		# toggle fullscreen
		if (key == 102 and key_modifiers == 2) or (key == 102 and key_modifiers == 10):
			#print(self.window.get_size())
			oldWidth, oldHeight=self.window.get_size()
			self.window.set_fullscreen(not self.window.fullscreen)
			width, height = self.window.get_size()
			#print(self.window.get_size())
			for elem in self.ui_manager._ui_elements:
				#elem.center_x = width/2
				if isinstance(elem, MenuBTN):
					elem.center_y= height-30
					elem.center_x= width-100
				else:
					elem.center_x = elem.center_x * (width/oldWidth)
					elem.center_y = elem.center_y * (height/oldHeight)
					#elem.center_x = sprite.center_x * (oldWidth//width)
					#elem.center_y = sprite.center_y * (oldHeight//)
					#elem.center_x= width
					#elem.center_y= height
					
			for sprite in self.sprites:
				sprite.center_x = sprite.center_x * (width/oldWidth)
				sprite.center_y = sprite.center_y * (height/oldHeight)

		# stop movimento player 1 semplice
		#if key == arcade.key.UP or key == arcade.key.DOWN:
		#	self.player1.change_y = 0
		#elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
		#	self.player1.change_x = 0

		# stop player 1 migliore
		if key == arcade.key.UP:
			self.up_pressed = False
		elif key == arcade.key.DOWN:
			self.down_pressed = False
		elif key == arcade.key.LEFT:
			self.left_pressed = False
		elif key == arcade.key.RIGHT:
			self.right_pressed = False
		# stop player 2
		if key == arcade.key.W:
			self.w_pressed = False
		elif key == arcade.key.S:
			self.s_pressed = False
		elif key == arcade.key.A:
			self.a_pressed = False
		elif key == arcade.key.D:
			self.d_pressed = False

	def drawGrid(self):
		width,height = self.window.get_size()
		OFFSETY= height/2 -256
		OFFSETX= width/2 -(448/2)
		MARGIN=0
		cellW=16
		cellH=16
		colors=[arcade.color.GREEN,arcade.color.WHITE,arcade.color.BLUE,arcade.color.BLACK]
		#crossPatter=0
		#print(self.grid[0][0])
		for row in range(gridRows):
			
			for column in range(gridCols):

				# Figure out what color to draw the box
				#if self.grid[row][column] == 1:
					#color = arcade.color.GREEN
				#else:
				#	color = arcade.color.WHITE
					# Do the math to figure out where the box is
				x = (cellW+MARGIN) * column + OFFSETX + cellW // 2
				y = (cellH+MARGIN) * row + OFFSETY +cellH // 2
					# Draw the box
				arcade.draw_rectangle_filled(x, y, cellW, cellW, colors[self.grid[row][column]])
	def resetGrid(self):
		#gridRows=31
		#gridCols=28
		#GRID VALUES: 0=empty path,1=coin path,2=wall,3=invalid
		#la griglia va dal basso verso l'alto
		
		#i miei occhi hanno perso 5 punti ciascuno per l'inizializzazione.
		self.grid[0]=[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
		self.grid[1]=[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
		self.grid[2]=[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2]
		self.grid[3]=[2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2]
		self.grid[4]=[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2]
		self.grid[5]=[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2]
		self.grid[6]=[2,2,2,1,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,1,2,2,2]
		self.grid[7]=[2,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,2]
		self.grid[8]=[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2]
		self.grid[9]=[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2]
		self.grid[10]=[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2]
		self.grid[11]=[2,2,2,2,2,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,2,2,2,2,2]
		self.grid[12]=[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3]
		self.grid[13]=[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3]
		self.grid[14]=[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3]
		self.grid[15]=[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2]
		self.grid[16]=[0,0,0,0,0,0,1,0,0,0,2,3,3,3,3,3,3,2,0,0,0,1,0,0,0,0,0,0]
		self.grid[17]=[2,2,2,2,2,2,1,2,2,0,2,3,3,3,3,3,3,2,0,2,2,1,2,2,2,2,2,2]
		self.grid[18]=[3,3,3,3,3,2,1,2,2,0,2,2,2,2,2,2,2,2,0,2,2,1,2,3,3,3,3,3]
		self.grid[19]=[3,3,3,3,3,2,1,2,2,0,0,0,0,0,0,0,0,0,0,2,2,1,2,3,3,3,3,3]
		self.grid[20]=[3,3,3,3,3,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,3,3,3,3,3]
		self.grid[21]=[2,2,2,2,2,2,1,2,2,2,2,2,0,2,2,0,2,2,2,2,2,1,2,2,2,2,2,2]
		self.grid[22]=[2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,2]
		self.grid[23]=[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2]
		self.grid[24]=[2,1,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,2,1,2]
		self.grid[25]=[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
		self.grid[26]=[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2]
		self.grid[27]=[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2]
		self.grid[28]=[2,1,2,2,2,2,1,2,2,2,2,2,1,2,2,1,2,2,2,2,2,1,2,2,2,2,1,2]
		self.grid[29]=[2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2]
		self.grid[30]=[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
		#self.grid
	def resetSprites(self):
		pass
		
class MenuBTN(arcade.gui.UIFlatButton):
	def on_click(self):
		
		global window3
		#print("ritorna pressed")
		window3.set_fullscreen(False)
		menu = menuView.MenuView(window3)
		window3.show_view(menu)

class DebugBTN(arcade.gui.UIFlatButton):
	def on_click(self):
		global debug
		debug= not debug
