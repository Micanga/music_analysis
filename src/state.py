from copy import deepcopy

class State:

	def __init__(self,histories):
		self.history = []
		for h in histories:
			self.history.append([elem for elem in h])

	def copy(self):
		new_state = State(self.history)
		return new_state
		