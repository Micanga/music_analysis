import matplotlib.pyplot as plt
import re

# 1. Retriving the data 
part_a, part_b, part_c = [], [], []
with open('cage_part_dados.csv') as cage_file:
	counter = 0
	for line in cage_file:
		info = line.split(',')

		new_list = []
		for x in info:
			if re.match('^\s*$',x) is None:
				if re.match('^\d+/\d+$',x) is None:
					new_list.append(float(x))
				else:
					new_list.append(float(x.split('/')[0])/float(x.split('/')[1]))

		# PART A
		if counter < 4:
			part_a.append(new_list)
		# PART B
		elif counter < 8:
			part_b.append(new_list)
		# PART C
		else:
			part_c.append(new_list)
		
		counter += 1

part_1, part_2, part_3, part_4 = [], [], [], []
for i in range(0,4):
	# PART 1
	if i == 0:
		part_1.append(part_a[i])
		part_1.append(part_b[i])
		part_1.append(part_c[i])
	# PART 2
	if i == 1:
		part_2.append(part_a[i])
		part_2.append(part_b[i])
		part_2.append(part_c[i])
	# PART 4
	if i == 2:
		part_3.append(part_a[i])
		part_3.append(part_b[i])
		part_3.append(part_c[i])
	# PART 4
	if i == 3:
		part_4.append(part_a[i])
		part_4.append(part_b[i])
		part_4.append(part_c[i])

# 2. Plotting
# Parte A 
fig, ax = plt.subplots(figsize=(8, 4))
plt.plot(part_a,  label=['Ciclo 1', 'Ciclo 2', 'Ciclo 3', 'Ciclo 4'])

# tidy up the figure
ax.grid(True)
ax.legend(loc='best')
ax.set_title('Parte A')
ax.set_xlabel('Valor do compasso')
ax.set_ylabel('Densidade')

plt.show()

# Parte B
fig, ax = plt.subplots(figsize=(8, 4))
plt.plot(part_b,  label=['Ciclo 1', 'Ciclo 2', 'Ciclo 3', 'Ciclo 4'])

# tidy up the figure
ax.grid(True)
ax.legend(loc='best')
ax.set_title('Parte B')
ax.set_xlabel('Valor do compasso')
ax.set_ylabel('Densidade')

plt.show()

# Parte C
fig, ax = plt.subplots(figsize=(8, 4))
plt.plot(part_c, label=['Ciclo 1', 'Ciclo 2', 'Ciclo 3', 'Ciclo 4'])

# tidy up the figure
ax.grid(True)
ax.legend(loc='best')
ax.set_title('Parte C')
ax.set_xlabel('Valor do compasso')
ax.set_ylabel('Densidade')

plt.show()

# Parte 1
fig, ax = plt.subplots(figsize=(8, 4))
plt.plot(part_1,  label=['Parte A', 'Part B', 'Part C'])

# tidy up the figure
ax.grid(True)
ax.legend(loc='best')
ax.set_title('Parte 1')
ax.set_xlabel('Valor do compasso')
ax.set_ylabel('Densidade')

plt.show()

# Parte 2
fig, ax = plt.subplots(figsize=(8, 4))
plt.plot(part_2,  label=['Parte A', 'Part B', 'Part C'])

# tidy up the figure
ax.grid(True)
ax.legend(loc='best')
ax.set_title('Parte 2')
ax.set_xlabel('Valor do compasso')
ax.set_ylabel('Densidade')

plt.show()

# Parte 3
fig, ax = plt.subplots(figsize=(8, 4))
plt.plot(part_3,  label=['Parte A', 'Part B', 'Part C'])

# tidy up the figure
ax.grid(True)
ax.legend(loc='best')
ax.set_title('Parte 3')
ax.set_xlabel('Valor do compasso')
ax.set_ylabel('Densidade')

plt.show()