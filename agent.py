import torch
import random, os, time, sys
import numpy as np
from collections import deque
from game import Game, Actions, ENTITIES, check_for_events
from model import Linear_QNet, QTrainer
from helper import plot
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
TARGET_GAMES=150
class Agent:

	def __init__(self):
		self.n_games = 0
		self.epsilon = 0.0 # randomness
		self.gamma = 0.5 # discount rate
		self.memory = deque(maxlen=MAX_MEMORY) # popleft()
		self.model = Linear_QNet(10, 300, 5)
		#meglio avere più parametri boolean che uno int, a quanto pare. [?] ricontrollare con nuova funzione check_ghost_is_coming
		self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
		self.n_games=0
	def get_state(self, game):
		
		pacman=game.entities[ENTITIES.PACMAN.value]
		red =game.entities[ENTITIES.RED.value]
		#pink=game.entities[ENTITIES.PINK.value]
		#can_move_arr=[int(game.can_move(Actions.LEFT,pacman)),int(game.can_move(Actions.RIGHT,pacman)),int(game.can_move(Actions.UP,pacman)),int(game.can_move(Actions.DOWN,pacman))]
		neightbours=game.get_neightbours(pacman)
		
		red_top=int(red.pos_in_grid_y > pacman.pos_in_grid_y)
		#pink_top=pink.pos_in_grid_y > pacman.pos_in_grid_y
		red_left=int(red.pos_in_grid_x < pacman.pos_in_grid_x)
		#pink_left=pink.pos_in_grid_x < pacman.pos_in_grid_x
		#print(str(can_move_arr))
		#cheese_list=[]
		#for action in Actions:
		#	if action != Actions.HALT:
		#		cheese_list.append(game.cheese_per_action(action,pacman))
		#biggest=cheese_list.index(max(cheese_list))
		#print(cheese_list)
		#print(biggest)
		red_danger_y,red_danger_x,ghost_facing=game.check_ghost_is_coming(red)
		#red_danger_y= int(red.pos_in_grid_y == pacman.pos_in_grid_y)
		#red_danger_x= int(red.pos_in_grid_y == pacman.pos_in_grid_y)
		#pink_danger_y,pink_danger_x,ghost_facing=game.check_ghost_is_coming(pink)
		#state=[int(red_danger_y),int(red_danger_x),int(pink_danger_y),int(pink_danger_y),*can_move_arr]
		#state=[red_top,red_left,red_danger_y,red_danger_x,*can_move_arr]
		#print(red_danger)
		#print(ghost_facing.value)
		#if red_danger_y:
		#	print("ROSSO VICINO Y")
		#if red_danger_x:
		#	print("ROSSO VICINO X")
		#state=[*can_move_arr,red_danger_y,red_danger_x,red_top,red_left,biggest]#,*neightbours_memory]
		#state=[red_danger_y,red_danger_x,red_top,red_left]
		#state=[*can_move_arr,red_danger_y,red_danger_x,biggest]#,*neightbours_memory]
		#state=[*can_move_arr,red_danger_y,red_danger_x,biggest,red_top,red_left]#,*neightbours_memory]
		
		cheese_top,cheese_left=game.get_closest_cheese()
		#print(cheese_top,cheese_left)

		#state=[*neightbours,red_danger_y,red_danger_x,red_top,red_left,cheese_top,cheese_left]
		state=[*neightbours,red_danger_y,red_danger_x,red_top,red_left,cheese_top,cheese_left]
		#state=[*can_move_arr,red_danger_y,red_danger_x,pink_danger_y,pink_danger_x,biggest]#,*neightbours_memory]

		#print(state)
		#state =[int(red_top),int(red_left),int(pink_top),int(pink_left),biggest]
		#state =[biggest]

		#print(state)
		return np.array(state, dtype=int)

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
	
	def get_action(self, state,is_traning):
		# random moves: tradeoff exploration / exploitation
		self.epsilon = TARGET_GAMES - self.n_games
		final_move = [0,0,0,0,0]
		#if self.epsilon < 20:
		#	self.epsilon= 20 # 10% minimum randomness
		if is_traning and random.randint(0, 200) <= self.epsilon:
			move = random.randint(0, 4)
			final_move[move] = 1
			return final_move
		else:
			state0 = torch.tensor(state, dtype=torch.float)
			prediction = self.model(state0)
			#if is_traning:
			move = torch.argmax(prediction).item()
			final_move[move] = 1
				#print(final_move)
			return final_move
 
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
	if not os.path.isfile(file_name):
		print("can't play without a saved model")
		sys.exit(1)
	#print(file_name)
	agent.model= torch.load(file_name) 
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
	f = open(file_name, "w")
	f.write(str(record))
	f.close()

def read_record():
	model_folder_path = 'model'
	#ricordo che model.pth DOVREBBE contenere gli state_dict, quindi il modello parziale.
	file_name = os.path.join(PATH,model_folder_path,'record.txt')
	if os.path.exists(file_name):
		f = open(file_name, "r")
		record=int(f.readline())
		#print(record)
		f.close()
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
		moves = agent.get_action(state_old,False)
		#print(prediction)
		#print(moves)
		if isinstance(moves, list):
			final_move=moves
		else:
			maybe_action=[0,0,0,0,0]
			sorted_indexes= torch.argsort(moves, descending= True)
			i=0
			maybe_action[sorted_indexes[i]]=1
			while game.can_move(maybe_action):
				maybe_action=[0,0,0,0,0]
				maybe_action[sorted_indexes[i]]=1
				i+=1
				#print("cambio azione perche' non fattibile")
			final_move=maybe_action
		reward, done, score = game.play_step(final_move)
		state_new = agent.get_state(game)

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
	while True:
		check_for_events(game)
		while not game.is_running:
			#game.check_for_input(final_move)
			check_for_events(game)
		state_old = agent.get_state(game)
		# get move
		moves = agent.get_action(state_old,True)
		#print(prediction)
		if isinstance(moves, list):
			final_move=moves
		else:
			maybe_action=[0,0,0,0,0]
			sorted_indexes= torch.argsort(moves, descending= True)
			i=0
			maybe_action[sorted_indexes[i]]=1
			while game.can_move(maybe_action):
				maybe_action=[0,0,0,0,0]
				maybe_action[sorted_indexes[i]]=1
				i+=1
				#print("cambio azione perche' non fattibile")
			final_move=maybe_action

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
			if score > record:
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
if __name__ == '__main__':
	PATH= os.path.dirname(__file__)
	os.chdir(PATH)
	train()
	#play()
