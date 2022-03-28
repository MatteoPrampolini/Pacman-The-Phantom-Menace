import torch
import random, os, time, sys
import numpy as np
from collections import deque
from entities import Pacman,FACING
from game import Game, Actions, ENTITIES, check_for_events, compare_int
from model import Linear_QNet, QTrainer
MAX_MEMORY = 100_000
BATCH_SIZE = 1000

class Agent:

	def __init__(self,lr = 0.015,target_games=70):
		self.n_games = 0
		self.epsilon = 0.0 # randomness
		self.gamma = 0.9 # discount rate	
		self.memory = deque(maxlen=MAX_MEMORY) # popleft()
		self.model = Linear_QNet(24,256, 5)
		self.trainer = QTrainer(self.model, lr=lr, gamma=self.gamma)
		self.target_games=target_games

	def get_state(self, game):
		
		pacman=game.entities[ENTITIES.PACMAN.value]
		red =game.entities[ENTITIES.RED.value]
		
		pink=game.entities[ENTITIES.PINK.value]
		neightbours=game.get_neightbours(pacman)
		red_top=compare_int(red.pos_in_grid_y,pacman.pos_in_grid_y)
		pink_top=compare_int(pink.pos_in_grid_y, pacman.pos_in_grid_y)
		red_left=compare_int(red.pos_in_grid_x, pacman.pos_in_grid_x)
		pink_left=compare_int(pink.pos_in_grid_x, pacman.pos_in_grid_x)

		state= [int(red.distance_from_pacman<3),int(pink.distance_from_pacman<3),int(red.distance_from_pacman<7),int(pink.distance_from_pacman<7),game.cheese_left,game.cheese_top,game.exit_top,game.exit_left,game.safe_exit,red_left,red_top,pink_left,pink_top,*neightbours,*game.possibilities,game.last_meaninful_action,red.facing.value,pink.facing.value] #pink_danger_y,red_danger_y

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
	
	def get_action(self, state, is_training=True):
			self.epsilon = self.target_games - self.n_games
			final_move = [0,0,0,0,0]
			if is_training and random.randint(0, 200) <= self.epsilon:
					move = random.randint(0, 4)
			else:
					state0 = torch.tensor(state, dtype=torch.float)
					prediction = self.model(state0)
					move = torch.argmax(prediction).item()
			final_move[move] = 1
			return final_move

 
def save_complete_model(agent):
	PATH= os.path.dirname(__file__)
	model_folder_path = 'model'
	file_name = os.path.join(PATH,model_folder_path,'complete.pth')
	if os.path.exists(file_name):
		os.remove(file_name)
	torch.save(agent.model, file_name)

def save_state_dict(agent):
	PATH= os.path.dirname(__file__)
	model_folder_path = 'model'
	file_name = os.path.join(PATH,model_folder_path,'model.pth')
	if os.path.exists(file_name):
		os.remove(file_name)
	torch.save(agent.model.state_dict(), file_name)

def load_state_dict(agent,game):
	game.should_run=False
	PATH= os.path.dirname(__file__)
	model_folder_path = 'model'
	file_name = os.path.join(PATH,model_folder_path,'model.pth')
	if not os.path.isfile(file_name):
		print("no previous model.pth found")
		write_record(0)
		return
	agent.model.load_state_dict(torch.load(file_name)) 
	game.reset()
	game.should_run=True
	agent.model.eval()
	print("model loaded")

def write_record(record):
	model_folder_path = 'model'
	file_name = os.path.join(PATH,model_folder_path,'record.txt')
	with open(file_name, "w") as f:
		f.write(str(record))

def read_record():
	PATH = os.path.dirname(__file__)
	model_folder_path = 'model'
	file_name = os.path.join(PATH,model_folder_path,'record.txt')
	if os.path.exists(file_name):
		with open(file_name, "r") as f:
			record=int(f.readline())
	else:
		record=0
	return record

def train(lr,target_games):
	PATH= os.path.dirname(__file__)
	os.chdir(PATH)
	record = 0
	agent = Agent(lr,target_games)
	game = Game()
	load_state_dict(agent,game)
	record=read_record()
	while game.quit == False:
		check_for_events(game)
		while not game.is_running:
			check_for_events(game)
		state_old = agent.get_state(game)
		moves = agent.get_action(state_old,is_training=True)
		final_move=moves
		reward, done, score = game.play_step(Actions(final_move))
		game.play_ghost()
		state_new = agent.get_state(game)
		
		# train short memory
		agent.train_short_memory(state_old, final_move, reward, state_new, done)
		# remember
		agent.remember(state_old, final_move, reward, state_new, done)
		if done:
			# train long memory
			game.reset()
			agent.n_games = game.n_games
			agent.train_long_memory() 
			if score >= record:
				record = score
				agent.model.save()
				write_record(record)
			if agent.n_games>=agent.target_games:
				save_complete_model(agent)
				save_state_dict(agent)
			print('Game', agent.n_games, 'This Score', score, 'Best Score:', record)

def play():

	print("Playing at my best!")
	train(lr = 0.001,target_games= -1)

if __name__ == '__main__':
	PATH= os.path.dirname(__file__)
	os.chdir(PATH)
	#train(lr = 0.015,target_games= 70)
	play()

