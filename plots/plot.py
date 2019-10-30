from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
from utils import *

# 1. Retriving the data 
part = load_part()
line = load_line()

# 2. Plotting Methods
def density_hist(data,label,title):
	fig, ax = plt.subplots(figsize=(8, 4))
	plt.hist(data, density=True, cumulative=False, label=label)
	ax.grid(True)
	ax.legend(loc='best')
	ax.set_title(title)
	ax.set_xlabel('Valor')
	ax.set_ylabel('Densidade')

	#mu = [np.mean(x) for x in data]
	#variance = [np.var(x) for x in data] 
	#sigma = [math.sqrt(x) for x in variance] 
	#x = [np.linspace(mu[i] - 3*sigma[i], mu[i] + 3*sigma[i], 100) for i in range(len(data))] 
	#for i in range(len(data)):
	#	plt.plot(x[i],stats.norm.pdf(x[i], mu[i], sigma[i]))

	plt.show()

density_hist(part[0],['Linha 1', 'Linha 2', 'Linha 3', 'Linha 4'],'Parte A')
density_hist(part[1],['Linha 1', 'Linha 2', 'Linha 3', 'Linha 4'],'Parte B')
density_hist(part[2],['Linha 1', 'Linha 2', 'Linha 3', 'Linha 4'],'Parte C')

density_hist(line[0],['Parte A','Parte B','Parte C'],'Linha 1')
density_hist(line[1],['Parte A','Parte B','Parte C'],'Linha 2')
density_hist(line[2],['Parte A','Parte B','Parte C'],'Linha 3')
density_hist(line[2],['Parte A','Parte B','Parte C'],'Linha 4')

def space_plotdef(data,title):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for x in data:
		for i in range(min([len(x[0]),len(x[1]),len(x)])):	
			ax.scatter(x[0][i],x[1][i],x[2][i])
	ax.grid(True)
	ax.legend(loc='best')
	ax.set_title(title)
	ax.set_xlabel('Parte A')
	ax.set_ylabel('Parte B')
	ax.set_zlabel('Parte C')

	plt.show()

space_plotdef(line,'Linha 1')