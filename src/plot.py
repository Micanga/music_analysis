import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as scisig
from utils import *
import sys

COMPASS = 8
ORDER = 6
NPARTS = 3
NFRIENDS = 4
ACTIONS = [0,1,2,3,4,5]

# 1. Retriving the data 
data = load_cumulative()
smooth_data = scisig.savgol_filter(data,(ORDER*COMPASS)-1,5,mode='nearest')
stddev = np.std(data - smooth_data)
upper_threshold = np.array(smooth_data + stddev) 
lower_threshold = np.array(smooth_data - stddev)

"""plt.figure(1,figsize=(8, 6))
plt.plot(data[:6*8],
		label= 'Discurso Extraido',
		color= 'black',
		linestyle= '-',
		marker = 'o',
		markersize=6,
		linewidth=3,
		clip_on=False)
plt.fill_between([i for i in range(6*8)], upper_threshold[:6*8],
		lower_threshold[:6*8],
		color='red', alpha=.35)
plt.plot(smooth_data[:6*8],
		label= 'Discurso Suavizado',
		color= 'red',
		linestyle= '-',
		marker = '',
		markersize=6,
		linewidth=6,
		clip_on=False)

plt.grid(True)
plt.legend(loc='best', fontsize=30,  \
		borderaxespad=0.3, borderpad=0.4, handletextpad=0.8, handlelength=0.5,\
		labelspacing=0.5, columnspacing=0.5,#mode='expand',\
		fancybox=True, framealpha=0.8, ncol=1)
#plt.title('Comulativo')
plt.xlabel('Compasso',fontsize=32)
plt.ylabel('Densidade Textural',fontsize=32)
axis = plt.gca()
axis.xaxis.set_tick_params(labelsize=18)
axis.yaxis.set_tick_params(labelsize=18)
plt.savefig("./plots/CI_A.png", bbox_inches='tight', pad_inches=0)
exit(1)"""

for r in range(1,10):
	cumulative_result = np.zeros(288)
	with open('resultMCT_'+str(r)+'.txt') as result_file:
		counter = 0
		for line in result_file:
			info = line.split(',')

			for i in range(4):
				cumulative_result[counter] += int(info[i])

			counter += 1

	smooth_result = scisig.savgol_filter(cumulative_result,(ORDER*COMPASS)-1,5,mode='nearest')

	# 3. Ploting the distribution
	plt.figure(r,figsize=(8, 6))
	plt.plot(smooth_data,
			label= 'Discurso Extraido (Base)',
			color= 'red',
			linestyle= '-',
			marker = '',
			markersize=6,
			linewidth=3,
			clip_on=False)
	plt.fill_between([i for i in range(288)], upper_threshold,
			lower_threshold,
			color='red', alpha=.35)

	plt.plot(smooth_result,
			label= 'Discurso Mimetizado',
			color= 'green',
			linestyle= '-',
			marker = '',
			markersize=6,
			linewidth=5,
			clip_on=False)
	plt.grid(True)
	plt.legend(loc='best', fontsize=14,  \
			borderaxespad=0.3, borderpad=0.4, handletextpad=0.8, handlelength=0.5,\
			labelspacing=0.5, columnspacing=0.5,#mode='expand',\
			fancybox=True, framealpha=0.8, ncol=1)
	#plt.title('Comulativo')
	plt.xlabel('Compasso',fontsize=20)
	plt.ylabel('Densidade Textural',fontsize=20)
	axis = plt.gca()
	axis.xaxis.set_tick_params(labelsize=12)
	axis.yaxis.set_tick_params(labelsize=12)
	plt.savefig("./plots/result"+str(r)+".png", bbox_inches='tight', pad_inches=0)
