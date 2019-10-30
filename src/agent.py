from copy import deepcopy
import numpy as np

from mcts import MCT, Node
from state import State

class Agent:

	def __init__(self,order,speach,nfriends,actions,main_id):
		self.actions = actions
		self.actions_probabilities = None
		self.history = []
		self.time = 0

		# 3. Monte-Carlo Application
		self.mct = MCT(main_id,300,150,self.actions,\
			order,speach,nfriends)

	def learn_probabilities(self,lines,selfline,nparts):
		# 1. Building actions probability matrix
		self.actions_probabilities = [[] for i in range(nparts)]
		for i in range(nparts):
			for j in range(len(lines)):
				self.actions_probabilities[i].append(np.zeros(len(self.actions)))

		# 2. Retrieving the actions probability from the
		# example piece
		for i in range(nparts):
			for j in range(len(lines)):
				for t in range(i*6*8*2,(i+1)*6*8*2):
					a = self.actions.index(lines[j][t])
					self.actions_probabilities[i][j][a] += 1

		# 3. Normalizing
		for j in range(len(lines)):
			for i in range(nparts):
				self.actions_probabilities[i][j] = \
				 self.actions_probabilities[i][j]/sum(self.actions_probabilities[i][j])

		# 4. Updating actions probabilities in the MCT
		self.mct.probabilities = deepcopy(self.actions_probabilities)
		self.mct.nparts = nparts

	def choose_action(self,simulation,main_time_step,counter):
		# 1. Planning the actions
		cur_state = State(simulation.history)
		self.mct.planning(cur_state,main_time_step,counter)

		# 2. Evaluating and returning the best action
		return self.mct.best_action(self.mct.root)