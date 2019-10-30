import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as scisig
from utils import *
import sys

from agent import Agent
from state import State

if len(sys.argv) > 1:
	experiment_number = sys.argv[1]
	print 'Experiment #'+experiment_number+'... ',
else:
	print 'fail'
	exit(1)
print 'ok'
sys.setrecursionlimit(2000)

COMPASS = 8
ORDER = 6
NPARTS = 3
NFRIENDS = 4
ACTIONS = [0,1,2,3,4,5]

# 1. Retriving the data 
# a. cumulative distribution
data = load_cumulative()

# b. smoothed cumulative dist and standard variation
smooth_data = scisig.savgol_filter(data,(ORDER*COMPASS)-1,5,mode='nearest')
stddev = np.std(data - smooth_data)

# c. line speach
lines = load_speach(NFRIENDS)


# 2. Preparing the action threshold
upper_threshold = np.array(smooth_data + stddev) 
lower_threshold = np.array(smooth_data - stddev)
speach = [upper_threshold,smooth_data,lower_threshold]

# 3. Ploting the distribution
"""plt.figure(figsize=(9, 5.5))
plt.plot(data,
		label= 'Discurso Puro (Discreto)',
		color= 'black',
		linestyle= '-',
		marker = 'o',
		markersize=6,
		linewidth=1,
		clip_on=False)
plt.plot(smooth_data,
		label= 'Discurso Extraido (Continuo)',
		color= 'red',
		linestyle= '-',
		marker = '',
		markersize=8,
		linewidth=5,
		clip_on=False)
plt.fill_between([i for i in range(288)], upper_threshold,
		lower_threshold,
		color='red', alpha=.35)
plt.grid(True)
plt.legend(loc='best', fontsize=14,  \
		borderaxespad=0.3, borderpad=0.4, handletextpad=0.8, handlelength=0.5,\
		labelspacing=0.5, columnspacing=0.5,#mode='expand',\
		fancybox=True, framealpha=0.8, ncol=1)
#plt.title('Comulativo')
plt.xlabel('Intervalo',fontsize=20)
plt.ylabel('Densidade Textural',fontsize=20)
axis = plt.gca()
axis.xaxis.set_tick_params(labelsize=12)
axis.yaxis.set_tick_params(labelsize=12)
plt.show()"""

# 4. Initializing the agents
agents = []
for i in range(NFRIENDS):
	agents.append(Agent(ORDER,speach,NFRIENDS,ACTIONS,i))
	agents[-1].learn_probabilities(lines,i,NPARTS)

# 5. Starting the piece online playing
max_time = sum([i*COMPASS*ORDER for i in [1,2,3]])
cur_state = State([[] for i in range(NFRIENDS)])
counter = [-1 for i in range(len(agents))]
for t in range(max_time):
	# a. choosing the action
	print '----- TIME:', t,'-----'
	round_actions = []
	for a in range(len(agents)):
		if agents[a].time <= t:
			action = agents[a].choose_action(cur_state,t,counter)

			agents[a].time += agents[a].mct.get_action_duration(action,agents[a].mct.root)

			agents[a].history.append(action)
			round_actions.append(action)
			#print a.mct.id,':',action
		else:
			if counter[a] == 0:
				counter[a] = -1
			else:
				counter[a] -= 1
			agents[a].history.append(agents[a].history[-1])
			round_actions.append(agents[a].history[-1])
			#print a.mct.id,':',a.history[-1]

	# b. updating current state
	for i in range(len(agents)):
		counter[i] = round_actions[i]
		cur_state.history[i].append(agents[i].history[-1])

	f = open("resultMCT_"+experiment_number+".txt", "a")
	#f.write(str(round_actions)+','+str(speach[1][t])+'\n')
	f.write(str(round_actions)+'\n')
	f.close()

#print cur_state.history
"""cumulative_result = np.zeros(288)
for i in range(288):
	for j in range(4):
		cumulative_result[i] += cur_state.history[j][i]

smooth_result = scisig.savgol_filter(cumulative_result,(ORDER*COMPASS)-1,5,mode='nearest')

plt.plot(smooth_result)
plt.plot(smooth_data)
plt.grid(True)
plt.legend(loc='best')
plt.title('Comulativo')
plt.xlabel('Intervalo')
plt.ylabel('Densidade')
plt.show()"""