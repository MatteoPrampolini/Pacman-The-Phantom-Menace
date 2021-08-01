import arcade, os, sys
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.ui_style import UIStyle
import startGame
import gameView
window2= None
class MenuView(arcade.View):		
	def __init__(self,window):
		super().__init__()
		self.ui_manager = UIManager()
		global window2
		window2=self.window
		self.setup()
		#self.fps=-1;
	def on_hide_view(self):
		self.ui_manager.unregister_handlers()

	def on_update(self, delta_time):
		
		pass
		#self.fps= round(1/delta_time)
		#if self.ui_manager._ui_elements[3].velocity == -1:  #usato come flag per chiudere il programma
		#	self.window.close()
		#	sys.exit(0)
	
	def on_draw(self):

		arcade.start_render()
		width,height= self.window.get_size()

		#arcade.draw_text("startGame", width/2 -156, height-100, arcade.color.BLUE, 50)
		#arcade.draw_text("fps: "+str(self.fps),10,height-30,arcade.color.WHITE,15)
		#arcade.draw_text("GIOCA", width/2 -128,height-150,arcade.color.WHITE,30)
		
		#self.startGame.draw()
		# Call draw() on all your sprite lists below

	def on_key_release(self, key, key_modifiers):
		"""
		Called whenever the user lets off a previously pressed key.
		"""
		#print(key, key_modifiers)
		#toggle fullscreen
		if (key == 102 and key_modifiers == 2) or (key == 102 and key_modifiers == 10):
			self.window.set_fullscreen(not self.window.fullscreen)
			width, height= self.window.get_size()
			for elem in self.ui_manager._ui_elements:
				elem.center_x = width/2



	def setup(self):
		self.ui_manager.purge_ui_elements()
		width,height= self.window.get_size()
		title= arcade.gui.UILabel(
		'PACMAN',
		center_x=width/2,
		center_y=height-30,
		)
		title.set_style_attrs(
			font_color=arcade.color.RED,
			font_color_hover=arcade.color.RED,
			font_color_press=arcade.color.RED,
			font_name='Arial',
			font_size= 50
		)
		self.ui_manager.add_ui_element(title)
		giocaBtn = PlayBTN(
			'Play',
			center_x=width/2,
			center_y=3/4 *height +50,
			width=250,
			height=40
		)
		self.ui_manager.add_ui_element(giocaBtn)
		settingsBtn = arcade.gui.UIFlatButton(
			'Settings',
			center_x=width/2,
			center_y=3/4* height,
			width=250,
			height=40
		)
		self.ui_manager.add_ui_element(settingsBtn)
		
		exitBtn = ExitBTN(
			'Exit',
			center_x= width/2,
			center_y= 3/4* height -50,
			width=250,
			height=40
		)
		self.ui_manager.add_ui_element(exitBtn)

class ExitBTN(arcade.gui.UIFlatButton):
	def on_click(self):
		#print("exit")
		arcade.close_window()
		
class PlayBTN(arcade.gui.UIFlatButton):
	def on_click(self):
		#print("play pressed")
		game = gameView.GameView(window2)
		window2.show_view(game)