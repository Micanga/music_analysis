import numpy as np
import re

def load_cumulative():
	cum = np.zeros(288)

	with open('data/cage_line_dados.csv') as cage_file:
		for line in cage_file:
			info = line.split(',')

			counter = 0
			for x in info:
				if re.match('^\s*$',x) is None:
					if re.match('^\d+/\d+$',x) is None:
						for i in range(int(x)):
							cum[counter] += int(x)
							counter += 1
					else:
						for i in range(int(x.split('/')[1])):
							cum[counter] += int(x.split('/')[0])
							counter += 1
							
	return cum

def load_speach(nfriends):
	speach = [np.zeros(288) for i in range(nfriends)]

	with open('data/cage_line_dados.csv') as cage_file:
		friend = 0
		for line in cage_file:
			info = line.split(',')

			counter = 0
			for x in info:
				if re.match('^\s*$',x) is None:
					if re.match('^\d+/\d+$',x) is None:
						for i in range(int(x)):
							speach[friend][counter] = int(x)
							counter += 1
					else:
						for i in range(int(x.split('/')[1])):
							speach[friend][counter] = int(x.split('/')[0])
							counter += 1
			friend += 1

	return speach

def load_part():
	part_a, part_b, part_c = [], [], []
	with open('data/cage_part_dados.csv') as cage_file:
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
	return [part_a,part_b,part_c]

def load_line():
	part_a, part_b, part_c = load_part()

	line_1, line_2, line_3, line_4 = [], [], [], []
	for i in range(0,4):
		# PART 1
		if i == 0:
			line_1.append(part_a[i])
			line_1.append(part_b[i])
			line_1.append(part_c[i])
		# PART 2
		if i == 1:
			line_2.append(part_a[i])
			line_2.append(part_b[i])
			line_2.append(part_c[i])
		# PART 4
		if i == 2:
			line_3.append(part_a[i])
			line_3.append(part_b[i])
			line_3.append(part_c[i])
		# PART 4
		if i == 3:
			line_4.append(part_a[i])
			line_4.append(part_b[i])
			line_4.append(part_c[i])

	return [line_1, line_2, line_3, line_4]