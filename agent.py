from matplotlib.pyplot import pause
import torch
import random, os, time, sys
import numpy as np
from collections import deque
from entities import Pacman,FACING
from game import Game, Actions, ENTITIES, check_for_events, compare_int
from model import Linear_QNet, QTrainer
from helper import plot
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
TARGET_GAMES= -70
def calculate_inting(pacman,ghost):
	if pacman.facing.value<2:
		same_danger_axis=abs(ghost.pos_in_grid_x - pacman.pos_in_grid_x)<=1
		#double_danger_pass= double_danger_pass and (ghost.pos_in_grid_x != pacman.pos_in_grid_x)
	else:
		same_danger_axis=abs(ghost.pos_in_grid_y - pacman.pos_in_grid_y)<=1
		#double_danger_pass= double_danger_pass and (ghost.pos_in_grid_y != pacman.pos_in_grid_y)
	#inting= [ghost.facing.value,pacman.facing.value] in [[0,1],[1,0],[2,3],[3,2]] #controllare inting
	ghost_getting_closer=ghost.distance_from_pacman < ghost.old_distance
	#inting= inting and ghost_getting_closer#same_danger_axis
	#inting=ghost_getting_closer and same_danger_axis
	return ghost_getting_closer, same_danger_axis
class Agent:

	def __init__(self):
		self.n_games = 0
		self.epsilon = 0.0 # randomness
		self.gamma = 0.9 # discount rate	
		self.memory = deque(maxlen=MAX_MEMORY) # popleft()
		self.model = Linear_QNet(24,256, 5)
		#meglio avere più parametri boolean che uno int, a quanto pare. [?] ricontrollare con nuova funzione check_ghost_is_coming
		self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
		self.n_games=0
	def get_state(self, game):
		
		pacman=game.entities[ENTITIES.PACMAN.value]
		red =game.entities[ENTITIES.RED.value]
		
		pink=game.entities[ENTITIES.PINK.value]
		#pink=game.entities[ENTITIES.RED.value] #DA TOGLIEREEEEEE
		#can_move_arr=[int(game.can_move(Actions.LEFT,pacman)),int(game.can_move(Actions.RIGHT,pacman)),int(game.can_move(Actions.UP,pacman)),int(game.can_move(Actions.DOWN,pacman))]
		neightbours=game.get_neightbours(pacman)
		red_top=compare_int(red.pos_in_grid_y,pacman.pos_in_grid_y)
		pink_top=compare_int(pink.pos_in_grid_y, pacman.pos_in_grid_y)
		red_left=compare_int(red.pos_in_grid_x, pacman.pos_in_grid_x)
		pink_left=compare_int(pink.pos_in_grid_x, pacman.pos_in_grid_x)
		
		#compare_ghost_top=compare_int(red.pos_in_grid_y,pink.pos_in_grid_y)
		#compare_ghost_left=compare_int(red.pos_in_grid_x,pink.pos_in_grid_x)

		#print(str(can_move_arr))
		#cheese_list=[]
		#for action in Actions:
		#	if action != Actions.HALT:
		#		cheese_list.append(game.cheese_per_action(action,pacman))
		#biggest=cheese_list.index(max(cheese_list))
		#print(cheese_list)
		#print(biggest)
		#red_warning_y,red_warning_x,ghost_facing=game.check_ghost_is_coming2(red)
		#red_warning=game.check_ghost_is_coming2(red)


		#red_danger_y= int(red.pos_in_grid_y == pacman.pos_in_grid_y)
		#red_danger_x= int(red.pos_in_grid_y == pacman.pos_in_grid_y)
		#pink_warning_y,pink_warning_x,ghost_facing=game.check_ghost_is_coming2(pink)
		#pink_warning=game.check_ghost_is_coming2(pink)
		#state=[int(red_danger_y),int(red_danger_x),int(pink_danger_y),int(pink_danger_y),*can_move_arr]
		#state=[red_top,red_left,red_danger_y,red_danger_x,*can_move_arr]
		#print(red_danger)
		#print(ghost_facing.value)
		#if red_danger_y:p
		#	print("ROSSO VICINO Y")
		#if red_danger_x:
		#	print("ROSSO VICINO X")
		#state=[*can_move_arr,red_danger_y,red_danger_x,red_top,red_left,biggest]#,*neightbours_memory]
		#state=[red_danger_y,red_danger_x,red_top,red_left]
		#state=[*can_move_arr,red_danger_y,red_danger_x,biggest]#,*neightbours_memory]
		#state=[*can_move_arr,red_danger_y,red_danger_x,biggest,red_top,red_left]#,*neightbours_memory]
		
		#self.cheese_top,cheese_left,cheese_dist=game.get_closest_cheese()
		#exit_top,exit_left=game.get_closest_safe_exit()
		#print(cheese_top,cheese_left,cheese_dist)
		#red_warning=game.is_ghost_in_the_corner(red,pacman)
		#pink_warning=game.is_ghost_in_the_corner(pink,pacman)
		#state=[*neightbours,red_danger_y,red_danger_x,red_top,red_left,cheese_top,cheese_left]
		#state=[*neightbours,red_danger_y,red_danger_x,red_top,red_left,cheese_top,cheese_left,pink_danger_y,pink_danger_x,pink_top,pink_left]
		#state=[*neightbours,red_danger_y,red_danger_x,red_top,red_left,pink_danger_y,pink_danger_x,pink_top,pink_left,red_warning_x,red_warning_y,pink_warning_x,pink_warning_y,pacman.invincible]
		
		# quello da 23 con corner
		# state=[red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,*red_warning,*pink_warning,*neightbours,red_top,red_left,pink_top,pink_left,cheese_top,cheese_left,pacman.invincible]
		#quello con rect
		#state=[red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,red_warning_y,red_warning_x,pink_warning_y,pink_warning_x,*neightbours,red_top,red_left,pink_top,pink_left,cheese_top,cheese_left,pacman.invincible]
		#rect no inv
		#state=[red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,red_warning_y,red_warning_x,pink_warning_y,pink_warning_x,*neightbours,red_top,red_left,pink_top,pink_left,cheese_top,cheese_left]
		#state=[red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,*red_warning,*pink_warning,*neightbours,red_top,red_left,pink_top,pink_left,cheese_top,cheese_left]
		#possibilities_red= game.can_go_in_there_before_ghost(red,pacman)
		#possibilities_pink= game.can_go_in_there_before_ghost(pink,pacman)
		#print(possibilities_pink)
		#print(game.possibilities)
		#state= [red_warning_y,red_warning_x,pink_warning_y,pink_warning_x,red_top,red_left,pink_top,pink_left,*game.possibilities,cheese_top,cheese_left]
		#state= [*game.possibilities,*neightbours,cheese_top,cheese_left,red_top,red_left,pink_top,pink_left,red_warning_y,red_warning_x,pink_warning_y,pink_warning_x]
		#state= [*game.possibilities,cheese_top,cheese_left]
		#old_action=pacman.old_action
		#old_action=pacman.old_action
		#print(pacman.old_action)
		
		#old_action= 0 if old_action==Actions.UP else 1 if old_action==Actions.DOWN else 2 if old_action==Actions.LEFT else 3 if old_action==Actions.RIGHT else 4 
		#print(old_action)
		red_facing=red.facing.value
		#red_facing
		#print(red.facing==FACING.SOUTH)
		#red_facing= 0 if red_facing==FACING.NORTH else 1 if red_facing==FACING.SOUTH else 2 if red_facing==FACING.WEST else 3 if red_facing==FACING.EAST else 4 
		pink_facing=pink.facing.value
		#pink_facing= 0 if pink_facing==FACING.NORTH else 1 if pink_facing==FACING.SOUTH else 2 if pink_facing==FACING.WEST else 3 if pink_facing==FACING.EAST else 4 
		
		#state= [*game.possibilities,*neightbours,red_top,red_left,pink_top,pink_left,red_warning_y,red_warning_x,pink_warning_y,pink_warning_x,game.unsure,old_action,game.safe_exit,cheese_top,cheese_left]
		#in questo stato ha bisogno di essere punito se corre dritto ai fantasmi
		#state= [*game.possibilities,red_top,red_left,pink_top,pink_left,game.safe_exit,cheese_top,cheese_left,old_action]
		#state= [*game.possibilities,*game.in_corner,cheese_top,cheese_left,red_top,red_left,pink_top,pink_left,red_warning_y,red_warning_x,pink_warning_y,pink_warning_x,game.safe_exit]
		#state= [red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,*game.possibilities,*game.in_corner,cheese_top,cheese_left,red_top,red_left,pink_top,pink_left,red_warning_y,red_warning_x,pink_warning_y,pink_warning_x,compare_ghost_top,compare_ghost_left,game.safe_exit,old_action]
		#game.get_ghost_distance()
		#print(game.red_dist,game.pink_dist)
		#state= [*neightbours,red_dist,pink_dist,exit_top,exit_left,game.safe_exit,*game.in_corner,red_top,pink_top,red_left,pink_left,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,*game.possibilities, cheese_top,cheese_left]
		#state= [red_warning_y,red_warning_x,pink_warning_y,pink_warning_x,game.stuck,game.safe_exit,exit_top,exit_left,*game.possibilities,*game.in_corner,game.red_getting_closer,game.pink_getting_closer,red_top,pink_top,red_left,pink_left,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x, cheese_top,cheese_left]
		#red_danger_y,red_danger_x=game.check_danger(red)
		#pink_danger_y,pink_danger_x=game.check_danger(pink)
		#state= [red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,*neightbours,*game.possibilities,*game.in_corner,red_top,pink_top,red_left,pink_left, cheese_top,cheese_left]
		#print(red_facing)
		#state= [*neightbours,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,red_facing,pink_facing,game.red_getting_closer,game.pink_getting_closer,old_action,*neightbours,*game.possibilities,*game.in_corner,red_top,pink_top,red_left,pink_left, cheese_top,cheese_left]
		red_danger_y,red_danger_x,facing=game.check_ghost_is_coming(red)
		pink_danger_y,pink_danger_x,facing=game.check_ghost_is_coming(pink)
		#state= [red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,game.red_getting_closer,game.pink_getting_closer,pacman.facing.value,*neightbours,red_warning,pink_warning,*game.possibilities,*game.in_corner,red_top,pink_top,red_left,pink_left, cheese_top,cheese_left]
		#state= [*neightbours,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,game.red_getting_closer,game.pink_getting_closer,pacman.facing.value,*game.possibilities,*game.in_corner,red_top,pink_top,red_left,pink_left, cheese_top,cheese_left]
		#state= [red.distance_from_pacman,pink.distance_from_pacman,red_warning,pink_warning,*neightbours,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,game.red_getting_closer,game.pink_getting_closer,pacman.facing.value,*game.possibilities,*game.in_corner,red_top,pink_top,red_left,pink_left, cheese_top,cheese_left]
		#state= [red_warning,pink_warning,*neightbours,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,game.red_getting_closer,game.pink_getting_closer,pacman.facing.value,*game.possibilities,*game.in_corner,red_top,pink_top,red_left,pink_left, cheese_top,cheese_left]
		#state= [game.safe_exit,*neightbours,*game.red_in_corner,*game.pink_in_corner,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,red_top,pink_top,red_left,pink_left, cheese_top,cheese_left]
		#state= [red_warning,pink_warning,old_action,game.stuck,game.safe_exit,*neightbours,*game.red_in_corner,*game.pink_in_corner,red_danger_y,red_top,pink_top,red_left,pink_left]
		#game.red_getting_closer

		red_getting_closer, red_close_axis=calculate_inting(pacman,red)
		pink_getting_closer, pink_close_axis=calculate_inting(pacman,pink)
		
		#print(game.possibilities, game.red_in_corner, game.pink_in_corner)
		#print(among_us)
		#state= [*game.possibilities,game.red_getting_closer,game.pink_getting_closer,red_warning,pink_warning,pacman.facing.value,red.facing.value,pink.facing.value,game.stuck,game.safe_exit,red_danger_y,red_top,pink_top,red_left,pink_left,cheese_left,cheese_top]
		#state= [*neightbours,*game.possibilities,pacman.facing.value,red.facing.value,pink.facing.value,red_danger_y,red_top,pink_top,red_left,pink_left,cheese_left,cheese_top]
		#state= [red.distance_from_pacman,pink.distance_from_pacman,game.exit_top,game.exit_left,game.safe_exit,game.stuck,red_getting_closer, red_close_axis,pink_getting_closer, pink_close_axis,*neightbours,*game.possibilities,game.last_meaninful_action,red.facing.value,pink.facing.value,red_danger_y,red_top,pink_top,red_left,pink_left,game.cheese_left,game.cheese_top]
		#state= [red.distance_from_pacman,pink.distance_from_pacman,pink_getting_closer, pink_close_axis,red_getting_closer, red_close_axis,game.exit_top,game.exit_left,game.safe_exit,game.stuck,*neightbours,*game.possibilities,game.last_meaninful_action,red.facing.value,pink.facing.value,pink_danger_y,red_danger_y,red_top,pink_top,red_left,pink_left,game.cheese_left,game.cheese_top]
		#state= [game.exit_top,game.exit_left,game.safe_exit,game.stuck, pink_close_axis,*neightbours,*game.possibilities,game.last_meaninful_action,red.facing.value,pink.facing.value,pink_danger_y,red_danger_y,red_top,pink_top,red_left,pink_left,game.cheese_left,game.cheese_top]
		#red_danger=game.check_ghost_is_coming2(red)
		#pink_danger=game.check_ghost_is_coming2(pink)
		#state= [pink_danger,red_danger,game.red_distance_lvl,game.pink_distance_lvl,game.exit_top,game.exit_left,game.sandwitch,game.safe_exit,game.cheese_left,game.cheese_top,red_left,red_top,pink_left,pink_top,*neightbours,*game.possibilities,game.last_meaninful_action,red.facing.value,pink.facing.value] #pink_danger_y,red_danger_y
		#state= [game.exit_top,game.exit_left,game.sandwitch,game.safe_exit,game.cheese_left,game.cheese_top,red_left,red_top,pink_left,pink_top,*neightbours,*game.possibilities,game.last_meaninful_action,red.facing.value,pink.facing.value] #pink_danger_y,red_danger_y
		#state= [red.distance_from_pacman,pink.distance_from_pacman,game.cheese_left,game.cheese_top,game.exit_top,game.exit_left,game.sandwitch,game.safe_exit,red_left,red_top,pink_left,pink_top,*neightbours,*game.possibilities,game.last_meaninful_action,red.facing.value,pink.facing.value] #pink_danger_y,red_danger_y
		state= [int(red.distance_from_pacman<3),int(pink.distance_from_pacman<3),int(red.distance_from_pacman<7),int(pink.distance_from_pacman<7),game.cheese_left,game.cheese_top,game.exit_top,game.exit_left,game.safe_exit,red_left,red_top,pink_left,pink_top,*neightbours,*game.possibilities,game.last_meaninful_action,red.facing.value,pink.facing.value] #pink_danger_y,red_danger_y

		#state= [red_warning,pink_warning,pacman.facing.value,red.facing.value,pink.facing.value,game.stuck,game.safe_exit,*neightbours,red_danger_y,red_top,pink_top,red_left,pink_left,cheese_left,cheese_top]

		#state= [game.stuck,game.safe_exit,exit_top,exit_left,*game.in_corner,*neightbours,game.red_getting_closer,game.pink_getting_closer,red_top,pink_top,red_left,pink_left,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x, cheese_top,cheese_left]

		#aggiungere dist formaggio + vicino e flag se ha solo 2 uscite (ovvero se non in turning point) (pericolo accherchiamento!)
		#state=[*neightbours,red_danger_y,red_danger_x,red_top,red_left,cheese_top,cheese_left,pink_danger_y,pink_danger_x,pink_top,pink_left,red_warning_x,red_warning_y,pink_warning_x,pink_warning_y,pacman.invincible]

		#state=[*can_move_arr,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,biggest]#,*neightbours_memory]

		#print(state)
		#state =[int(red_top),int(red_left),int(pink_top),int(pink_left),biggest]
		#state =[biggest]
	
		#print(red_dist)
		#arr = np.array(['a','b'])
		#print(arr.dtype)
		#input()
		#al posto dei danger e warning restituire un array boolean che dice se pacman arriva prima a nodo di ghost red.
		return np.array(state, dtype='i1') #-127,128

	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

	def train_long_memory(self):
		
		if len(self.memory) > BATCH_SIZE:
			mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
		else:
			mini_sample = self.memory

		states, actions, rewards, next_states, dones = zip(*mini_sample)
		self.trainer.train_step(states, actions, rewards, next_states, dones)
		
	def train_short_memory(self, state, action, reward, next_state, done):
		self.trainer.train_step(state, action, reward, next_state, done)
	
	def get_action(self, state,is_traning,pacman):
			#print(pacman)
			#am_i_running_down= state[0]+state[1]+state[2]+state[3]
			#am_i_running_down= state[4]+state[5]+state[6]+state[7]
			#se siamo in pericolo puoi cambiare direzione, altrimenti scegli quella predefinita fino al prossimo incrocio
			#am_i_running_down= state[0]+state[1]+state[2]+state[3]+state[4]+state[5]+state[6]+state[7]+state[8]+state[9]+state[10]+state[11]

			#if not is_in_turning_point(pacman):
					#print("old:"+str(pacman.old_action.value))
					#print(pacman.old_action.value)
					#print(final_move)
					#print("continuo"+str(pacman.old_action))
			#		return pacman.old_action.value
			# random moves: tradeoff exploration / exploitation
			self.epsilon = TARGET_GAMES - self.n_games
			#self.epsilon=0 #TOGLIEREEEE
			#if self.epsilon < 20:
			#	self.epsilon= 20 # 10% minimum randomness
			#if is_traning and random.randint(0, 450) <= self.epsilon:
			final_move = [0,0,0,0,0]
			if is_traning and random.randint(0, 200) <= self.epsilon:
					move = random.randint(0, 4)
			else:
					state0 = torch.tensor(state, dtype=torch.float)
					prediction = self.model(state0)
					#if is_traning:
					move = torch.argmax(prediction).item()
			final_move[move] = 1
			#print(final_move)
			return final_move
			#return final_move
			#pacman.old_action 
 
def save_complete_model(agent):
	PATH= os.path.dirname(__file__)
	model_folder_path = 'model'
	#ricordo che model.pth DOVREBBE contenere gli state_dict, quindi il modello parziale.
	file_name = os.path.join(PATH,model_folder_path,'complete.pth')
	if os.path.exists(file_name):
		os.remove(file_name)
	torch.save(agent.model, file_name)
	print("saved")

def load_complete_model(agent,game):
	game.should_run=False
	PATH= os.path.dirname(__file__)
	model_folder_path = 'model'
	#ricordo che model.pth DOVREBBE contenere gli state_dict, quindi il modello parziale.
	file_name = os.path.join(PATH,model_folder_path,'complete.pth')
	#file_name2 = os.path.join(PATH,model_folder_path,'model.pth')

	if not os.path.isfile(file_name):
		print("can't play without a saved model")
		sys.exit(1)
	#print(file_name)
	agent.model= torch.load(file_name) 
	#agent.model= torch.load
	#agent.model.load_state_dict(file_name2)
	game.reset()
	game.should_run=True
	agent.model.eval()
	
	print("loaded")
def save_state_dict(agent):
	PATH= os.path.dirname(__file__)
	model_folder_path = 'model'
	#ricordo che model.pth DOVREBBE contenere gli state_dict, quindi il modello parziale.
	file_name = os.path.join(PATH,model_folder_path,'model.pth')
	if os.path.exists(file_name):
		os.remove(file_name)
	torch.save(agent.model.state_dict(), file_name)
	print("saved")
def load_state_dict(agent,game):
	game.should_run=False
	PATH= os.path.dirname(__file__)
	model_folder_path = 'model'
	#ricordo che model.pth DOVREBBE contenere gli state_dict, quindi il modello parziale.
	file_name = os.path.join(PATH,model_folder_path,'model.pth')
	if not os.path.isfile(file_name):
		print("no previous model.pth found")
		write_record(0)
		#sys.exit(1)
	#print(file_name
	else:
		agent.model.load_state_dict(torch.load(file_name)) 
		game.reset()
		game.should_run=True
		agent.model.eval()
		print("loaded")

def write_record(record):
	model_folder_path = 'model'
	#ricordo che model.pth DOVREBBE contenere gli state_dict, quindi il modello parziale.
	file_name = os.path.join(PATH,model_folder_path,'record.txt')
	with open(file_name, "w") as f:
		f.write(str(record))

def read_record():
	model_folder_path = 'model'
	#ricordo che model.pth DOVREBBE contenere gli state_dict, quindi il modello parziale.
	file_name = os.path.join(PATH,model_folder_path,'record.txt')
	if os.path.exists(file_name):
		with open(file_name, "r") as f:
			record=int(f.readline())
	else:
		record=0
	return record
def play():
	PATH= os.path.dirname(__file__)
	os.chdir(PATH)
	total_score = 0
	record = 0
	agent = Agent()
	game = Game()
	load_complete_model(agent,game)
	while True:
		#print(final_move)
		state_old = agent.get_state(game)
		#print(state_old)
		# get move
		moves = agent.get_action(state_old,True,game.entities[0])

		#print(prediction)
		#print(moves)

		#if isinstance(moves, list):
		#	final_move=moves
		#else:
			#maybe_action=[0,0,0,0,0]
			#sorted_indexes= torch.argsort(moves, descending= True)
			#i=0
			#maybe_action[sorted_indexes[i]]=1
			#while game.can_move(maybe_action):
			#	maybe_action=[0,0,0,0,0]
			#	maybe_action[sorted_indexes[i]]=1
			#	i+=1
			#	#print("cambio azione perche' non fattibile")
			#final_move=maybe_action
		#print(Actions(final_move))
		reward, done, score = game.play_step(Actions(moves))
		game.play_ghost()
		state_new = agent.get_state(game)
		#agent.train_short_memory(state_old, moves, reward, state_new, done)
		# remember
		#agent.remember(state_old, moves, reward, state_new, done)
		# train short memory
		#agent.train_short_memory(state_old, final_move, reward, state_new, done)

		# remember
		#agent.remember(state_old, final_move, reward, state_new, done)
		
		if done or game.score<=0:
			# train long memory, plot result
			game.reset()
			agent.n_games += 1
			#agent.train_long_memory()

def train():
	PATH= os.path.dirname(__file__)
	os.chdir(PATH)
	plot_scores = []
	plot_mean_scores = []
	total_score = 0
	record = 0
	agent = Agent()
	game = Game()
	model_folder_path = './model'
	#ricordo che model.pth contiene gli state_dict, quindi il modello parziale.
	#https://pytorch.org/tutorials/beginner/saving_loading_models.html
	file_name = os.path.join(model_folder_path,'model.pth')
	load_state_dict(agent,game)
	record=read_record()
	print("previous record:"+str(record))
	while True:#record<2440:
		check_for_events(game)
		while not game.is_running:
			#game.check_for_input(final_move)
			check_for_events(game)
		state_old = agent.get_state(game)
		# get move
		moves = agent.get_action(state_old,True,game.entities[0])
		final_move=moves
		#print(prediction)
		# if isinstance(moves, list):
		# 	final_move=moves
		# else:
		# 	maybe_action=[0,0,0,0,0]
		# 	sorted_indexes= torch.argsort(moves, descending= True)
		# 	i=0
		# 	maybe_action[sorted_indexes[i]]=1
		# 	while game.can_move(maybe_action):
		# 		maybe_action=[0,0,0,0,0]
		# 		maybe_action[sorted_indexes[i]]=1
		# 		i+=1
		# 		#print("cambio azione perche' non fattibile")
		# 	final_move=maybe_action

		# perform move and get new state
		
		#print(Actions(final_move).name)
		#SCHIFO DEBUG
		#print("---")
		#can_mov_arr=np.array([state_old[0],state_old[1],state_old[2],state_old[3]])
		#lista = np.where(can_mov_arr == 1)[0]
		#left,right,up,down
		#dire=""
		#if 0 in lista:
		#	dire+="left "
		#if 1 in lista:
			# dire+="right "
		# if 2 in lista:
			# dire+="up "
		# if 3 in lista:
			# dire+="down "			
		# #print("possible moves: "+dire)
		# if state_old[4]:
			# print("DANGER Y")
		# if state_old[5]:
			# print("DANGER X")			
		#print(*state_old[:4])
		#input()
	
		reward, done, score = game.play_step(Actions(final_move))
		game.play_ghost()
		#print(reward)
		#print(reward,done,score)
		#print(game.entities[0],final_move,game.can_move(final_move,game.entities[0]))
		state_new = agent.get_state(game)
		
		# train short memory
		agent.train_short_memory(state_old, final_move, reward, state_new, done)
		# remember
		agent.remember(state_old, final_move, reward, state_new, done)
		if done:
			# train long memory, plot result
			game.reset()
			#game.n_games +=1
			agent.n_games = game.n_games
			agent.train_long_memory()
			#score= score - timer
			#score= score 
			if score >= record:
				record = score
				agent.model.save()
				write_record(record)
			if agent.n_games>=TARGET_GAMES:
				save_complete_model(agent)
				save_state_dict(agent)
			print('Game', agent.n_games, 'This Score', score, 'Best Score:', record)

			#plot_scores.append(score)
			#total_score += score
			#mean_score = total_score / agent.n_games
			#plot_mean_scores.append(mean_score)
			#plot(plot_scores, plot_mean_scores)
	#save_state_dict(agent)
	#save_complete_model(agent)
	#print("FINITO")
if __name__ == '__main__':
	PATH= os.path.dirname(__file__)
	os.chdir(PATH)
	train()
	#play()

