from copy import deepcopy
from math import sqrt, log
from numpy.random import choice
from numpy.random import uniform

class MCT:

	def __init__(self, main_id, max_it, max_depth,\
	 actions,order,speach,nfriends):
		self.id = main_id

		self.max_it = max_it
		self.max_depth = max_depth
		self.root = None

		self.actions = actions
		self.probabilities = None
		self.nparts = 0
		self.order = order
		self.speach = speach
		self.nfriends = nfriends

	def planning(self,current_state,main_time_step,counter):
		counter[self.id] = -1

		# 1. Checking and updating the root
		if not self.root:
			self.root = Node(None,main_time_step,current_state,0,None)
		else:
			self.root = self.update_root(self.root,current_state)
			if self.root is None:
				self.root = Node(None,main_time_step,current_state,0,None)
			else:
				self.root.parent = None

		# 2. Performing simulations into the tree
		# searching for best action
		for it in range(self.max_it):
			start_counter = [c for c in counter]
			self.search(self.root,self.id,start_counter)

	def update_root(self,root,current_state):
		min_len = min([len(current_state.history[k]) for k in range(self.nfriends)])

		path = []
		for i in range(min_len):	
			for j in range(self.nfriends):
				path.append(current_state.history[j][i])

		new_root = self.root
		for choose in path:
			walk_flag = False
			#print choose, [c.action for c in new_root.children]
			for c in new_root.children:
				if c.action == choose:
					walk_flag = True
					new_root = c
					break
			if walk_flag == False:
				#print 'No path'
				return None

		#print 'Path'
		return new_root

	def search(self,node,cur_id,counter):
		# 1. Checking the MC-stop condition
		if self.is_terminal(node.time) or self.is_leaf(node):
			return 0

		# 2. Selecting a action for the MC simulation
		if counter[cur_id] == -1:
			action = self.select_action(node,cur_id)
			counter[cur_id] = self.get_action_duration(action,node)
		elif not node.parent:
			return 0
		else:
			action = node.state.history[cur_id][-1]
			counter[cur_id] -= 1

		# 4. Performing a simulation using the select action
		next_state, reward = self.simulate_action(action,cur_id,node)
		
		# 5. Stepping on the next node (defined by the simulation)
		next_node = node.get_action_child(action)
		if not next_node:
			next_node = Node(action,node.time+1,next_state,node.depth+1,node)
			node.children.append(next_node)
		#print 'action:',action,'; depth:',next_node.depth,'; reward:',reward

		# 6. Calculating the utility (q-value) for the current node
		# and updating it
		discount_factor = 0.95
		new_counter = [elem for elem in counter]
		q_value = (reward) + (discount_factor *\
			self.search(next_node,(cur_id+1)%self.nfriends,new_counter))
		node.value = q_value
		node.visits += 1

		return q_value

	def is_terminal(self,cur_time):
		return True if cur_time >= 288 else False

	def is_leaf(self,node):
		return True if node.depth >= self.max_depth else False

	def get_action_duration(self,action,node):
		part = node.get_part()
		if action == 5:
			return action + 3
		elif action == 4:
			return action + 2
		elif action == 0:
			if part == 0:
				return 6
			else:
				return 8
		else:
			return action

	def select_action(self,node,cur_id):
		# 1. Retrieving the node part and time
		time = node.time
		part = node.get_part()

		# 2. Checking untried actions
		untried_actions = []
		for i in range(len(self.actions)):
			if self.probabilities[part][cur_id][i] > 0:
				untried_actions.append(self.actions[i])

		for c in node.children:
			untried_actions.remove(c.action)

		# 2. If exist untried actions,
		# choose an untried action
		if len(untried_actions) > 0:
			action = choice(untried_actions)
			return action

		# 3. Else perform the bias selection
		if cur_id == self.id:
			return self.uct_select_action(node)
		else:
			return self.weightedChoice(cur_id,node)	

	def uct_select_action(self,node):
		maxUCB = -9999999
		maxA   = None

		# 1. Getting the valid actions
		valid_actions = []
		part = node.get_part()
		for i in range(len(self.actions)):
			if self.probabilities[part][self.id][i] > 0:
				valid_actions.append(self.actions[i])

		# 2. Applying UCT evaluation
		for a in valid_actions:
			child = node.get_action_child(a)
			if child:
				if (child.visits > 0):
					currentUCB = child.value+ 0.5 * sqrt(
						log(float(node.visits)) / float(child.visits))
				else:
					currentUCB = 0

				if maxUCB < (-currentUCB):
					maxUCB = (-currentUCB)
					maxA = child.action
				elif maxUCB < currentUCB:
					maxUCB = currentUCB
					maxA = child.action
			else:
				return a

		# 3. Returing an action
		if not maxA and len(node.state.history[self.id]) > 0:
			maxA = self.weightedChoice(self.id,node)
		elif maxA is None:
			maxA = choice(valid_actions)

		return maxA

	def weightedChoice(self,cur_id,node):
		# 0. Getting valid actions
		valid_actions = []
		part = node.get_part()
		for i in range(len(self.actions)):
			if self.probabilities[part][cur_id][i] > 0:
				valid_actions.append(self.actions[i])

		# 1. Calculating the cumulative vector
		# a. appending the probabilities
		cum = []
		for i in range(len(self.actions)):
			cum.append(self.probabilities[part][cur_id][i])

		# b. checking restriction
		if sum(cum) == 0:
			return choice(valid_actions)

		# c. normalazing
		if sum(cum) != 1:
			cum = cum/sum(cum)

		# d. cumulative probabilities
		for i in range(1,len(cum)):
			cum[i] += cum[i-1]

		# 2. Doing the weighted choice
		coin = uniform(0,1)
		for i in range(len(cum)):
			if coin < cum[i]:
				return self.actions[i]

	def simulate_action(self,action,cur_id,node):
		# 1. Calculating the action probability
		# and getting friends action
		part = node.get_part()

		friends = []
		action_probability = self.probabilities[part][cur_id][self.actions.index(action)]
		if node.time > 0:
			for i in range(self.nfriends):
				if len(node.state.history[i]) > 0:
					if cur_id != i:
						friends.append(node.state.history[i][-1])

		# 2. Updating current agent history
		tmp_state = node.state.copy()
		tmp_state.history[cur_id].append(action)

		# 3. Calculating the reward
		cur_speach = int(action)+sum(friends)
		reward = action_probability*(1/(abs(self.speach[1][node.time]-cur_speach)+1))

		#if self.speach[0][node.time] < cur_speach\
		#or self.speach[2][node.time] > cur_speach:
		#	reward -= 1
		#else:
		#	reward += 1

		return tmp_state, reward

	def best_action(self,node):
		max_value = -99999
		action = None

		for c in node.children:
			if max_value < c.value:
				max_value = c.value
				action = c.action

		if action is None:
			action = self.weightedChoice(self.id,node)

		return action

class Node:

	 def __init__(self, action, time, state, depth, parent=None):
	 	self.parent = parent
	 	self.children = [] 
	 	self.depth = depth
	 	self.time = time

	 	self.action = action
	 	self.state = state
	 	self.value = 0
	 	self.visits = 0

	 def get_action_child(self,action):
	 	for c in self.children:
	 		if c.action == action:
	 			return c

	 def get_part(self):
	 	if self.time < 6*8*2:
	 		return 0
	 	elif self.time < 2*6*8:
	 		return 1
	 	else:
	 		return 2