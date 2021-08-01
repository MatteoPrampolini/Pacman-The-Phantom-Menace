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

#nel gioco di default prime 3 e ultime 2 rows sono vuote.
class GameView(arcade.View):		
	def __init__(self,window):
		super().__init__()
		self.ui_manager = UIManager() #buttons, text e simili
		self.sprites = arcade.SpriteList() #le sprite
		self.grid = []
		for row in range(gridRows):
			self.grid.append([])
			for column in range(gridCols):
				self.grid[row].append(1)
		#print(self.grid)
		#print(self.grid[0][0])
		self.resetGrid()
		self.fps=-1;
		#self.
		global window3
		window3=self.window
		#sprites
		self.setup()
	
	def on_hide_view(self):
		self.ui_manager.unregister_handlers()
			
		
	def on_update(self, delta_time):
		self.fps= round(1/delta_time)
	def on_key_release(self, key, key_modifiers):
		#print(key, key_modifiers)
		#toggle fullscreen
		
		if (key == 102 and key_modifiers == 2) or (key == 102 and key_modifiers == 10):
			#print(self.window.get_size())
			oldWidth, oldHeight=self.window.get_size()
			self.window.set_fullscreen(not self.window.fullscreen)
			width, height= self.window.get_size()
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
		
	def on_draw(self):
		
		arcade.start_render()
		self.sprites.draw()
		if debug:
			self.drawGrid()
		width,height= self.window.get_size()
		
		arcade.draw_text("fps: "+str(self.fps),10,height-30,arcade.color.WHITE,15)
		arcade.draw_text("NAPOLI",100,height-30,arcade.color.WHITE,15)
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
		#self.sprites.append(arcade.Sprite(startGame.PATH+'/assets/map.png', scale=1.0, center_x=width/2, center_y=height/2))
	def drawGrid(self):
		width,height= self.window.get_size()
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
