import arcade, os, sys
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.ui_style import UIStyle
import gameView
import menuView
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "CRACKMAN"
PATH= os.path.dirname(__file__)
window= None

class CrackManGame(arcade.View):

	def __init__(self, window):
		super().__init__()
		#self.tick=0
		#self.fps=-1;
		self.crackman = None
		self.window = window
		arcade.set_background_color(arcade.color.EERIE_BLACK)

		# If you have sprite lists, you should create them here,
		# and set them to None
		self.player_list = None
		self.player = None



	def on_update(self, delta_time):
		"""
		All the logic to move, and the game logic goes here.
		Normally, you'll call update() on the sprite lists that
		need it.
		"""
		#self.tick=self.tick+1
		self.fps= round(1/delta_time)
		#print(self.fps)


		pass

	
	def on_draw(self):
		"""
		Render the screen.
		"""

		# This command should happen before we start drawing. It will clear
		# the screen to the background color, and erase what we drew last frame.
		arcade.start_render()
		width,height= self.window.get_size()
		arcade.draw_text("CRACKMAN", width/2 -128, height-100, arcade.color.BLUE, 50)
		#arcade.draw_text("tick: "+str(self.tick),10,height-50,arcade.color.WHITE,15)
		arcade.draw_text("fps: "+str(self.fps),10,height-30,arcade.color.WHITE,15)
		self.crackman.draw()
		# Call draw() on all your sprite lists below



	def on_key_release(self, key, key_modifiers):
		"""
		Called whenever the user lets off a previously pressed key.
		"""
		#print(key, key_modifiers)
		#toggle fullscreen
		if (key == 102 and key_modifiers == 2) or (key == 102 and key_modifiers == 10):
			self.window.set_fullscreen(not self.window.fullscreen)
			#update sprite center
			width,height= self.window.get_size()
			self.crackman.center_x = width/2
			self.crackman.center_y = height/2


	def setup(self):
		""" Set up the game variables. Call to re-start the game. """
		# Create your sprites and sprite lists here
		#commento un attimo sta parte per testing, credo non sia troppo utile
		#self.crackman = arcade.Sprite(PATH+'\\assets\crackman.png', 0.5)
		#width,height= self.window.get_size()
		#self.crackman.center_x = width/2
		#self.crackman.center_y = height/2

		#parte tek

		self.player_list = arcade.SpriteList()
		self.player = arcade.AnimatedTimeSprite()
		self.player.textures = []

		for i in range(3):
			self.player.textures.append(arcade.load_texture("sprites/sprites.png", x=900, y=i*45, width=45, height=45))

		width, height = self.window.get_size()
		self.player.center_x = width // 2
		self.player.center_y = height // 2

		self.player_list.append(self.player)

#il menu del gioco



	
		
def main():
	#os.chdir(PATH)
	global window
	window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	#start_view=  CrackManGame(window)
	#window.show_view(start_view)
	#start_view.setup()
	#print(dir(window))
	menu_view=  menuView.MenuView(window)
	window.show_view(menu_view)
	menu_view.setup()
	arcade.run()


if __name__ == "__main__":
	main()